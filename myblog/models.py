from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True) # db_index=True - индексация для более быстрого поиска
    slug = models.SlugField(max_length=150, unique=True) # unique=True - уникальность, SlugField - типа чарфилд, но с валидатором
                                         # (большие маленькие буквы, цыфры, нижнее подчеркивание,дифис и все)
    body = models.TextField(blank=True, db_index=True) # blank=True- полк может быть пустым, db_index=True - индексация для более быстрого поиска
    date_pub = models.DateTimeField(auto_now_add=True) # auto_now_add=True - текуущее время при сохранении в базу,
                                                       # auto_now=True - будет менятся при каждом изменении

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заголовок"
        verbose_name_plural = "Заголовки"