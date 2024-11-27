from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArtistListView.as_view(), name='artist-list'),
    path('<int:pk>/', views.ArtistDetailView.as_view(), name='artist-detail'),
    path('new/', views.ArtistCreateView.as_view(), name='artist-create'),
    path('<int:pk>/edit/', views.ArtistUpdateView.as_view(), name='artist-update'),
    path('<int:pk>/delete/', views.ArtistDeleteView.as_view(), name='artist-delete'),
    path('<int:pk>/portfolio/', views.ArtistPortfolioView.as_view(), name='artist-portfolio'),
]