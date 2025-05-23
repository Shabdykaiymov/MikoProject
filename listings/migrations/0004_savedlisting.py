# Generated by Django 5.1.7 on 2025-05-09 15:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_alter_category_name_alter_listing_address_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата сохранения')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_by_users', to='listings.listing', verbose_name='Объявление')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_listings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сохраненное объявление',
                'verbose_name_plural': 'Сохраненные объявления',
                'unique_together': {('user', 'listing')},
            },
        ),
    ]
