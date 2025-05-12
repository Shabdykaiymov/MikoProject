from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):
    map_address = forms.CharField(
        label='Адрес на карте',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите адрес или выберите на карте',
            'id': 'map_address'
        })
    )

    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'contact_info', 'image', 'category', 'address']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название объявления'
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Подробное описание товара/услуги'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена в сомах',
                'min': 0
            }),
            'contact_info': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телефон или email для связи'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'address': forms.HiddenInput(attrs={
                'id': 'id_address'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'title': 'Название объявления',
            'description': 'Описание',
            'price': 'Цена (С)',
            'contact_info': 'Контактная информация',
            'image': 'Изображение',
            'category': 'Категория',
            'address': ''
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

        # Если редактируем объект и у него уже есть адрес — подставим в поле карты
        if self.instance and self.instance.address:
            self.fields['map_address'].initial = self.instance.address

    def clean(self):
        cleaned_data = super().clean()
        map_address = cleaned_data.get('map_address')

        if map_address:
            cleaned_data['address'] = map_address

        return cleaned_data
