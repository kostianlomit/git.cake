from datetime import timezone

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse



class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст работы")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Выпечку'
        verbose_name_plural = 'Выпечка'
        ordering = ['id']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})



class Work(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст работы")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('work_detail', args=[self.id])

    class Meta:
        verbose_name = 'Работу'
        verbose_name_plural = 'Работы'
        ordering = ['id']





class Images(models.Model):
    id = models.AutoField
    object_id = models.PositiveIntegerField(null=True, default=1)
    post = models.ForeignKey(Work, null=True, blank=True, verbose_name="Работа", on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='media/%Y/%m/%d/')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=20)
    content_object = GenericForeignKey("content_type", "object_id")
    class Meta:
        verbose_name = 'Фото к статье'
        verbose_name_plural = 'Фото к статьям'


class About(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст работы")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('about', args=[self.id])

    class Meta:
        verbose_name = 'О сайте'
        verbose_name_plural = 'О сайте'
        ordering = ['id']




class Comment(models.Model):
    post = models.ForeignKey(Women, on_delete=models.PROTECT, related_name='коментарии')
    name = models.CharField(max_length=80,verbose_name="Имя")
    email = models.EmailField()
    body = models.TextField(verbose_name="Текст")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)



