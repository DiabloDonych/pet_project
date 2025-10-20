from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm, AvatarForm
from django.urls import reverse
from .models import Genre, Anime, Format, Year, Episode, Favorite
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Anime, Comment
from .forms import CommentForm
import json
from django.views.decorators.csrf import csrf_exempt

def homePage(request):
    return render(request, "user/banner.html")

def topAnime(request):
    anime = Anime.objects.all()[:1]
    animes = Anime.objects.all()[:10]

    return render(request, "user/top-anime.html", {
        'anime': anime,
        'animes': animes
    })

def allAnime(request):
    query = request.GET.get('q', '').strip()
    genre_slug = request.GET.get('genre')
    year_value = request.GET.get('year')
    format_slug = request.GET.get('format')
    sort_rating = request.GET.get('sort_rating')

    if query:
        animes = Anime.objects.filter(Q(animeName__icontains=query))
        if not animes.exists():
            no_results = True
        else:
            no_results = False
    else:
        animes = Anime.objects.all()
        no_results = False
        if genre_slug:
            animes = animes.filter(genre__slug=genre_slug)
        if year_value:
            animes = animes.filter(year__yearValue=year_value)
        if format_slug:
            animes = animes.filter(format__slug=format_slug)
        if sort_rating:
            if sort_rating == 'asc':
                animes = animes.order_by('rating')
            elif sort_rating == 'desc':
                animes = animes.order_by('-rating')

    genres = Genre.objects.all()
    formats = Format.objects.all()
    years = Year.objects.all()

    return render(request, 'user/all-anime.html', {
        'animes': animes,
        'genres': genres,
        'formats': formats,
        'years': years,
        'query': query,
        'no_results': no_results
    })

def animeDetail(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    comments = Comment.objects.filter(anime=anime).order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.anime = anime
                comment.save()
                return redirect('animeDetail', pk=anime.pk)
        else:
            return redirect('loginPage')
    else:
        form = CommentForm()

    return render(request, "user/anime-detail.html", {
        'anime': anime,
        'comments': comments,
        'form': form
    })

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('homePage')
    else:
        form = SignUpForm()
    return render(request, 'auth/sign-up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homePage')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

@login_required
def profile(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('anime')
    return render(request, 'user/profile.html', {'favorites': favorites})

@login_required
def change_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AvatarForm(instance=request.user.profile)
    return render(request, 'user/change_avatar.html', {'form': form})


@login_required
@require_POST
def toggle_favorite(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    user = request.user

    favorite, created = Favorite.objects.get_or_create(user=user, anime=anime)

    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite})

def logout_view(request):
    logout(request)
    return redirect(reverse('homePage'))

@csrf_exempt
def edit_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            data = json.loads(request.body)
            comment.text = data['text']
            comment.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'You do not have permission to edit this comment.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
