from django.db import models
from django.shortcuts import reverse


class Post(models.Model):
    # Поля которые тут создаем передаются в конструктор класс models.Model
    tags_to_post = models.ManyToManyField('Tag', blank=True, related_name="posts_to_tag") # blank=True- полк может быть пустым,
                                                    # related_name - имя для обратной связи, то свойство что появится у модели Tag

    title = models.CharField(max_length=150, db_index=True) # db_index=True - индексация для более быстрого поиска
    slug = models.SlugField(max_length=150, unique=True) # unique=True - уникальность, SlugField - типа чарфилд, но с валидатором
                                         # (большие маленькие буквы, цыфры, нижнее подчеркивание,дифис и все)
    body = models.TextField(blank=True, db_index=True) # blank=True- полк может быть пустым, db_index=True - индексация для более быстрого поиска
    date_pub = models.DateTimeField(auto_now_add=True) # auto_now_add=True - текуущее время при сохранении в базу,
                                                       # auto_now=True - будет менятся при каждом изменении

    def get_absolute_url(self):  # метод который возвращает ссылку на конкретный обьет класса, передаем url шаблона и словарь
        return reverse("post_detail_url", kwargs={"slug": self.slug})  # в словарь в качестве ключа получает slug,
                                                                       # то поле по которому мы проводим идентификацию обьекта и self.slug
                                                                       # (поле конкретно обьекта )
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заголовок"
        verbose_name_plural = "Заголовки"


class Tag(models.Model):
    title = models.CharField(max_length=150, db_index=True)  # db_index=True - индексация для более быстрого поиска
    slug = models.SlugField(max_length=150, unique=True)  # unique=True - уникальность, SlugField - типа чарфилд, но с валидатором


    def get_absolute_url(self):
        return reverse("tag_detail_url", kwargs={"slug": self.slug})


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"