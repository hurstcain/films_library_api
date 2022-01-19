from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.serializers import ValidationError


class Films(models.Model):
    """
    Абстрактный класс для моделей Movie и TV
    title - название фильма или сериала
    year - год выпуска
    rating - оценка
    genre - жанры
    """

    title = models.CharField(max_length=200)
    year = models.IntegerField(
        validators=[
            MaxValueValidator(2030),
            MinValueValidator(1880)
        ]
    )
    genre = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f'{self.pk}, {self.title}'

    class Meta:
        abstract = True
        ordering = ['title']


class TV(Films):
    """
    Модель сериалов
    number_of_episodes - количество эпизодов
    avg_episode_duration - средняя длина одного эпизода
    added_by - внешний ключ, поле, в котором содержится информация о пользователе, который добавил сериал в базу данных
    """

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
    """
    Модель фильмов
    duration - продолжительность фильма
    added_by - внешний ключ, поле, в котором содержится информация о пользователе, который добавил фильм в базу данных
    """

    duration = models.IntegerField(blank=True, null=True)
    added_by = models.ForeignKey('auth.User', related_name='movies_added', on_delete=models.CASCADE)


class FilmsWatchedAndFilmsToWatchAbstractClass(models.Model):
    """
    Абстрактный класс для моделей FilmsWatched и FilmsToWatch
    user - пользователь, который добавил запись в БД, внешний ключ
    tv - сериал, который был добавлен в список, внешний ключ
    movie - фильм, который был добавлен в список, внешний ключ
    Одновременно запись может содержать не пустое поле либо фильма, либо сериала.
    """

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tv = models.ForeignKey(TV, null=True, blank=True, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)

    def is_movie(self) -> bool:
        """
        Функция проверяет содержит ли запись данные о фильме
        """

        if self.movie is not None:
            return True
        else:
            return False

    def is_tv(self) -> bool:
        """
            Функция проверяет содержит ли запись данные о сериале
        """

        if self.tv is not None:
            return True
        else:
            return False

    def __str__(self) -> str:
        if self.tv is not None:
            return f'{self.user}, {self.tv}'
        elif self.movie is not None:
            return f'{self.user}, {self.movie}'

    class Meta:
        abstract = True
        ordering = ['user']
        unique_together = [['user', 'tv'], ['user', 'movie']]


class FilmsWatched(FilmsWatchedAndFilmsToWatchAbstractClass):
    """
    Фильмы и сериалы, которые были просмотрены пользователями
    user - пользователь, который добавил запись, внешний ключ
    score - оценка пользователя
    review - обзор пользователя
    """

    user = models.ForeignKey('auth.User', related_name='films_watched', on_delete=models.CASCADE)
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
        """
        На всякий случай перед сохранением записи в БД добавлена проверка, что поля и фильма и сериала
        не были выбраны одновременно, а также что оба этих поля не пусты
        """

        if self.tv is None and self.movie is None:
            raise ValidationError('Укажите фильм или сериал')
        elif self.tv is not None and self.movie is not None:
            raise ValidationError('Укажите или фильм или сериал')
        else:
            if self.tv is not None:
                obj = FilmsToWatch.objects.filter(tv=self.tv, user=self.user)
                if obj:
                    obj.delete()
            elif self.movie is not None:
                obj = FilmsToWatch.objects.filter(movie=self.movie, user=self.user)
                if obj:
                    obj.delete()
            super(FilmsWatched, self).save(*args, **kwargs)


class FilmsToWatch(FilmsWatchedAndFilmsToWatchAbstractClass):
    """
    Фильмы и сериалы, которые добавлены в список желаемых к просмотру
    user - пользователь, который добавил запись, внешний ключ
    """

    user = models.ForeignKey('auth.User', related_name='films_to_watch', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        На всякий случай перед сохранением записи в БД добавлена проверка, что поля и фильма и сериала
        не были выбраны одновременно, а также что оба этих поля не пусты
        """

        if self.tv is None and self.movie is None:
            raise ValidationError('Укажите фильм или сериал')
        elif self.tv is not None and self.movie is not None:
            raise ValidationError('Укажите или фильм или сериал')
        else:
            if self.tv is not None:
                if FilmsWatched.objects.filter(tv=self.tv, user=self.user):
                    raise ValidationError('Вы уже посмотрели данный сериал')
            elif self.movie is not None:
                if FilmsWatched.objects.filter(movie=self.movie, user=self.user):
                    raise ValidationError('Вы уже посмотрели данный фильм')
            super(FilmsToWatch, self).save(*args, **kwargs)
