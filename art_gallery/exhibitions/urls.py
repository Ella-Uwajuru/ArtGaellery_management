from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExhibitionListView.as_view(), name='exhibition-list'),
    path('<int:pk>/', views.ExhibitionDetailView.as_view(), name='exhibition-detail'),
    path('new/', views.ExhibitionCreateView.as_view(), name='exhibition-create'),
    path('<int:pk>/edit/', views.ExhibitionUpdateView.as_view(), name='exhibition-update'),
    path('<int:pk>/delete/', views.ExhibitionDeleteView.as_view(), name='exhibition-delete'),
    path('<int:exhibition_id>/manage-artwork/', views.manage_exhibition_artwork, name='manage-exhibition-artwork'),
]