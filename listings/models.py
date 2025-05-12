from django.db import models
from django.contrib.auth.models import User
import requests
from django.conf import settings
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    @classmethod
    def get_default_categories(cls):
        """Возвращает список категорий по умолчанию"""
        return [
            'Еда',
            'Животные',
            'Недвижимость',
            'Техника',
            'Работа',
            'Услуги',
            'Транспорт'
        ]

    @classmethod
    def create_default_categories(cls):
        """Создает категории по умолчанию"""
        for category_name in cls.get_default_categories():
            cls.objects.get_or_create(name=category_name)


class Listing(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    contact_info = models.CharField(max_length=255, verbose_name='Контактная информация')
    image = models.ImageField(
        upload_to='listings/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name='Категория'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Полный адрес',
        help_text='Введите адрес или выберите на карте'
    )
    latitude = models.FloatField(blank=True, null=True, editable=False, verbose_name='Широта')
    longitude = models.FloatField(blank=True, null=True, editable=False, verbose_name='Долгота')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        if self.address and not (self.latitude and self.longitude):
            self.geocode_address()
        if self.address and not (self.latitude and self.longitude):
            raise ValidationError({
                'address': 'Не удалось определить координаты для указанного адреса.'
            })

    def save(self, *args, **kwargs):
        if self.address and not (self.latitude and self.longitude):
            self.geocode_address()
        super().save(*args, **kwargs)

    def geocode_address(self):
        if not self.address or not hasattr(settings, 'YANDEX_MAPS_API_KEY'):
            return

        try:
            api_key = settings.YANDEX_MAPS_API_KEY
            url = f"https://geocode-maps.yandex.ru/1.x/?format=json&apikey={api_key}&geocode={self.address}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            feature = data['response']['GeoObjectCollection']['featureMember'][0]
            pos = feature['GeoObject']['Point']['pos']
            self.longitude, self.latitude = map(float, pos.split())
            self.address = feature['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        except (requests.RequestException, KeyError, IndexError) as e:
            self.latitude = None
            self.longitude = None
            print(f"Ошибка геокодирования: {e}")

    def get_map_url(self):
        if self.latitude and self.longitude:
            return f"https://yandex.ru/maps/?pt={self.longitude},{self.latitude}&z=16&l=map"
        return None


class SavedListing(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='saved_listings',
        verbose_name='Пользователь'
    )
    listing = models.ForeignKey(
        'Listing',
        on_delete=models.CASCADE,
        related_name='saved_by_users',
        verbose_name='Объявление'
    )
    saved_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата сохранения')

    class Meta:
        verbose_name = 'Сохраненное объявление'
        verbose_name_plural = 'Сохраненные объявления'
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"
