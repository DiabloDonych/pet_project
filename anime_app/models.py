from django.db import models
from django.contrib.auth.models import User
from pytils.translit import slugify

class Genre(models.Model):
    genreName = models.CharField("Genre name", max_length=255)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def __str__(self):
        return self.genreName

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.genreName)
            original_slug = self.slug
            for x in range(1, 100):
                if not Genre.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f'{original_slug}-{x}'
        super().save(*args, **kwargs)

class Format(models.Model):
    formatName = models.CharField("Format name", max_length=255)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def __str__(self):
        return self.formatName

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.formatName)
            original_slug = self.slug
            for x in range(1, 100):
                if not Format.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f'{original_slug}-{x}'
        super().save(*args, **kwargs)

class Year(models.Model):
    yearValue = models.IntegerField("Year", unique=True)

    def __str__(self):
        return str(self.yearValue)

class Anime(models.Model):
    animeName = models.CharField("Anime name", max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Genre")
    format = models.ForeignKey(Format, on_delete=models.CASCADE, verbose_name="Format", default=1)
    cover = models.CharField("Link to cover", max_length=500)
    poster = models.CharField("Link to poster", max_length=500)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, verbose_name="Year")
    rating = models.FloatField("Rating")
    animeLink = models.CharField("YouTube", max_length=500)
    description = models.TextField("Description")
    inTrend = models.BooleanField('Intrend', default=False, blank=True, null=True)
    bestSeason = models.BooleanField('Best of the season', default=False)

    def __str__(self):
        return self.animeName

class Episode(models.Model):
    anime = models.ForeignKey(Anime, related_name='episodes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    episode_number = models.IntegerField()
    video_link = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.anime.animeName} - Episode {self.episode_number}: {self.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')

    def __str__(self):
        return self.user.username

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user.username} - {self.anime.animeName}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

