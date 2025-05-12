# initial_data.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mikomarket.settings')
django.setup()

from listings.models import Category

def create_categories():
    categories = [
        'Электроника',
        'Одежда',
        'Недвижимость',
        'Транспорт',
        'Мебель',
        'Бытовая техника',
        'Услуги',
        'Хобби и отдых',
        'Животные',
        'Другое'
    ]
    
    for category_name in categories:
        Category.objects.get_or_create(name=category_name)
    
    print(f'Создано {len(categories)} категорий')

if __name__ == '__main__':
    print('Начало заполнения базы данных...')
    create_categories()
    print('Заполнение завершено!')
