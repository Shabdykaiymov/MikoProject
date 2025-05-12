from django.urls import path
from . import views

urlpatterns = [
    path('saved-listings/', views.saved_listings, name='saved_listings'),
    path('', views.home, name='home'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/new/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/update/', views.update_listing, name='update_listing'),
    path('listing/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
    path('listing/<int:pk>/save/', views.save_listing, name='save_listing'),
    path('saved/', views.saved_listings, name='saved_listings'),
]
