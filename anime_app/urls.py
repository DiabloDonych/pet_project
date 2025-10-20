from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import edit_comment, delete_comment

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('anime/top/', views.topAnime, name='topAnime'),
    path('anime/all/', views.allAnime, name='allAnime'),
    path('anime/all/filter/<slug:slug>', views.allAnime, name='filterAnime'),
    path('anime/detail/<int:pk>/', views.animeDetail, name='animeDetail'),
    path('user/sign-up/', views.sign_up, name='signUp'),
    path('user/login/', views.login_view, name='loginPage'),
    path('user/logout/', views.logout_view, name='logout'),
    path('comments/edit/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('profile/', views.profile, name='profile'),
    path('anime/<int:pk>/', views.animeDetail, name='animeDetail'),
    path('profile/change-avatar/', views.change_avatar, name='change_avatar'),
    path('favorites/toggle/<int:anime_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
