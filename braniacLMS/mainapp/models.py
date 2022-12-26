from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _



class News(models.Model):
    title = models.CharField(max_length=256, verbose_name=_('Заголовок'))
    preamble = models.CharField(max_length=1024, verbose_name=_('Интро'))
    body = models.TextField(verbose_name=_('Содержимое'))
    body_as_markdown = models.BooleanField(default=False, verbose_name=_('Разметка в формате Markdown'))  # Тип разметки

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создан'))  # Зполняется при комите в базу
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Обновлен'))
    deleted = models.BooleanField(default=False, verbose_name=_('Удалено'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class Course(models.Model):
    title = models.CharField(max_length=256, verbose_name=_('Заголовок'))
    description = models.TextField(verbose_name=_('Описание'))
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Стоимость'), default=0)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создан'))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Обновлен'))
    deleted = models.BooleanField(default=False, verbose_name=_('Удалено'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_('Курс'))
    num = models.PositiveIntegerField(default=0, verbose_name=_('Номер урока'))

    title = models.CharField(max_length=256, verbose_name=_('Заголовок'))
    description = models.TextField(verbose_name=_('Описание'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создан'))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Обновлен'))
    deleted = models.BooleanField(default=False, verbose_name=_('Удалено'))

    def __str__(self):
        return f'{self.num} {self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class CourseTeacher(models.Model):
    course = models.ManyToManyField(Course)

    first_name = models.CharField(max_length=256, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=256, verbose_name=_('Фамилия'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создан'))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Обновлен'))
    deleted = models.BooleanField(default=False, verbose_name=_('Удалено'))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'курс к учителю'
        verbose_name_plural = 'курсы к учителям'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class CourseFeedback(models.Model):
    RATINGS = (
        (5, "⭐⭐⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (3, "⭐⭐⭐"),
        (2, "⭐⭐"),
        (1, "⭐")
    )

    rating = models.SmallIntegerField(choices=RATINGS, default=5, verbose_name=_('Рейтинг'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_("Курс"))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    feedback = models.TextField(default="Без отзыва", verbose_name=_("Отзыв"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''


    def __str__(self):
        return f"Отзыв на {self.course} от {self.user}"
