"""
Main models
"""

from django.db import models
# from django.urls import path
# from django.urls import include
# from django.http import HttpResponse
from django.core.exceptions import ValidationError


def validate_even(val):
    if val % 2 != 0:
        raise ValidationError(f'The {val} is not even', code='odd', params={'val': val})


class Bb(models.Model):
    """
    Model of boards
    """
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, validators=[validate_even], verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Show description of goods')

        if not self.price or self.price < 0:
            errors['price'] = ValidationError('Insert a positive price')

        if errors:
            raise ValidationError(errors)


class MinMaxValueValidator:
    """
    Validation
    """
    def __init__(self, minVal, maxVal):
        self.min_val = minVal
        self.max_val = maxVal

    def __call__(self, val):
        if val < self.min_val or val > self.max_val:
            raise ValidationError(f"Val must be > {self.min_val} and less than {self.max_val}",
            code='out_of_range',
            params={'minVal':self.min_val, 'maxVal':self.max_val})


class Rubric(models.Model):
    """
    Rubrics
    """
    name = models.CharField(max_length=50, db_index=True, verbose_name='Название')

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

    def __str__(self):
        return self.name

    
