from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArtworkListView.as_view(), name='artwork-list'),
    path('<int:pk>/', views.ArtworkDetailView.as_view(), name='artwork-detail'),
    path('new/', views.ArtworkCreateView.as_view(), name='artwork-create'),
    path('<int:pk>/edit/', views.ArtworkUpdateView.as_view(), name='artwork-update'),
    path('<int:pk>/delete/', views.ArtworkDeleteView.as_view(), name='artwork-delete'),
]