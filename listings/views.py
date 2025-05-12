from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Listing, Category, SavedListing
from .forms import ListingForm
import logging

# Настройка логгера
logger = logging.getLogger(__name__)

def home(request):
    try:
        categories = Category.objects.all()
        listings = Listing.objects.select_related('category', 'user').order_by('-created_at')

        category_id = request.GET.get('category')
        if category_id:
            listings = listings.filter(category_id=category_id)

        search_query = request.GET.get('q')
        if search_query:
            listings = listings.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        context = {
            'listings': listings,
            'categories': categories,
            'selected_category': int(category_id) if category_id else None,
            'search_query': search_query or ''
        }
        return render(request, 'listings/home.html', context)

    except Exception as e:
        logger.error(f"[HOME VIEW] Ошибка: {str(e)}", exc_info=True)
        messages.error(request, 'Ошибка при загрузке главной страницы.')
        return redirect('home')

def listing_detail(request, pk):
    try:
        listing = get_object_or_404(Listing, pk=pk)
        related_listings = Listing.objects.filter(category=listing.category).exclude(pk=pk).order_by('-created_at')[:4]

        return render(request, 'listings/listing_detail.html', {
            'listing': listing,
            'related_listings': related_listings
        })

    except Exception as e:
        logger.error(f"[DETAIL VIEW] Ошибка: {str(e)}", exc_info=True)
        messages.error(request, 'Ошибка при загрузке объявления.')
        return redirect('home')

@login_required
def create_listing(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                listing = form.save(commit=False)
                listing.user = request.user
                listing.save()
                messages.success(request, '✅ Объявление успешно создано!')
                return redirect('listing_detail', pk=listing.pk)
            except ValidationError as e:
                messages.error(request, f'Ошибка: {str(e)}')
    else:
        form = ListingForm()

    return render(request, 'listings/create_listing.html', {'form': form, 'categories': categories})

@login_required
def save_listing(request, pk):
    try:
        listing = get_object_or_404(Listing, pk=pk)
        saved_listing, created = SavedListing.objects.get_or_create(user=request.user, listing=listing)
        if created:
            messages.success(request, '✅ Объявление добавлено в сохранённые!')
        else:
            messages.info(request, 'Это объявление уже в сохранённых!')

        return redirect('listing_detail', pk=pk)

    except Exception as e:
        logger.error(f"[SAVE VIEW] Ошибка при сохранении объявления: {str(e)}", exc_info=True)
        messages.error(request, 'Ошибка при добавлении в сохранённые.')
        return redirect('listing_detail', pk=pk)

def saved_listings(request):
    try:
        saved_listings = SavedListing.objects.filter(user=request.user).select_related('listing')
        return render(request, 'listings/saved_listings.html', {
            'saved_listings': saved_listings,
            'title': 'Сохранённые объявления'
        })

    except Exception as e:
        logger.error(f"[SAVED LISTINGS VIEW] Ошибка при загрузке сохранённых объявлений: {str(e)}", exc_info=True)
        messages.error(request, 'Ошибка при загрузке сохранённых объявлений.')
        return redirect('home')

# Добавление функции для обновления объявления
@login_required
def update_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if request.user != listing.user:
        messages.error(request, 'Ошибка: У вас нет прав для редактирования этого объявления.')
        return redirect('listing_detail', pk=listing.pk)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Объявление обновлено!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)

    return render(request, 'listings/create_listing.html', {'form': form, 'categories': Category.objects.all()})

# Добавление функции для удаления объявления
@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if request.user != listing.user:
        messages.error(request, 'Ошибка: У вас нет прав для удаления этого объявления.')
        return redirect('listing_detail', pk=listing.pk)

    if request.method == 'POST':
        listing.delete()
        messages.success(request, '✅ Объявление удалено!')
        return redirect('home')

    return render(request, 'listings/delete_listing.html', {'listing': listing})
def saved_listings(request):
    # Получаем все сохранённые объявления для текущего пользователя
    saved_items = SavedListing.objects.filter(user=request.user)
    return render(request, 'listings/saved_listings.html', {'saved_items': saved_items})