from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator


class Films(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField(
        validators=[
            MaxValueValidator(2030),
            MinValueValidator(1880)
        ]
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    genre = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.pk}, {self.title}'

    class Meta:
        abstract = True
        ordering = ['title']


class TV(Films):
    number_of_episodes = models.IntegerField(
        blank=True,
        validators=[
            MinValueValidator(1)
        ],
        null=True
    )
    avg_episode_duration = models.IntegerField(blank=True, null=True)
    added_by = models.ForeignKey('auth.User', related_name='tv_added', on_delete=models.CASCADE)


class Movie(Films):
    duration = models.IntegerField(blank=True, null=True)
    added_by = models.ForeignKey('auth.User', related_name='movies_added', on_delete=models.CASCADE)


class FilmsWatched(models.Model):
    user = models.ForeignKey('auth.User', related_name='films_watched', on_delete=models.CASCADE)
    tv = models.ForeignKey(TV, null=True, blank=True, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    review = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.tv is None and self.movie is None:
            raise AssertionError('Укажите фильм или сериал')
        elif self.tv is not None and self.movie is not None:
            raise AssertionError('Укажите или фильм или сериал')
        else:
            super(FilmsWatched, self).save(*args, **kwargs)

    def is_movie(self):
        if self.movie is not None:
            return True
        else:
            return False

    def is_tv(self):
        if self.tv is not None:
            return True
        else:
            return False

    def __str__(self):
        if self.tv is not None:
            return f'{self.user}, {self.tv}'
        elif self.movie is not None:
            return f'{self.user}, {self.movie}'

    class Meta:
        ordering = ['user']
        unique_together = ('user', 'tv', 'movie')


class FilmsToWatch(models.Model):
    user = models.ForeignKey('auth.User', related_name='films_to_watch', on_delete=models.CASCADE)
    tv = models.ForeignKey(TV, null=True, blank=True, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.tv is None and self.movie is None:
            raise AssertionError('Укажите фильм или сериал')
        elif self.tv is not None and self.movie is not None:
            raise AssertionError('Укажите или фильм или сериал')
        else:
            super(FilmsToWatch, self).save(*args, **kwargs)

    def is_movie(self):
        if self.movie is not None:
            return True
        else:
            return False

    def is_tv(self):
        if self.tv is not None:
            return True
        else:
            return False

    def __str__(self):
        if self.tv is not None:
            return f'{self.user}, {self.tv}'
        elif self.movie is not None:
            return f'{self.user}, {self.movie}'

    class Meta:
        ordering = ['user']
        unique_together = ('user', 'tv', 'movie')
