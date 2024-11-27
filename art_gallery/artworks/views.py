from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Artwork
from django.shortcuts import redirect
from django.contrib import messages  # Add this import
from .forms import ArtworkForm
from django.db.models import Q

class ArtworkListView(ListView):
    model = Artwork
    template_name = 'artworks/artwork_list.html'
    context_object_name = 'artworks'
    paginate_by = 12

    def get_queryset(self):
        queryset = Artwork.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

class ArtworkDetailView(DetailView):
    model = Artwork
    template_name = 'artworks/artwork_detail.html'
    context_object_name = 'artwork'
    
class ArtworkCreateView(LoginRequiredMixin, CreateView):
    model = Artwork
    form_class = ArtworkForm
    template_name = 'artworks/artwork_form.html'
    success_url = reverse_lazy('artwork-list')

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'artist'):
            messages.error(request, 'You need to create an artist profile before adding artworks.')
            return redirect('artist-create')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.artist = self.request.user.artist
        return super().form_valid(form)

class ArtworkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Artwork
    form_class = ArtworkForm
    template_name = 'artworks/artwork_form.html'

    def test_func(self):
        artwork = self.get_object()
        return self.request.user == artwork.artist.user

    def get_success_url(self):
        return reverse_lazy('artwork-detail', kwargs={'pk': self.object.pk})
class ArtworkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Artwork
    template_name = 'artworks/artwork_confirm_delete.html'
    success_url = reverse_lazy('artwork-list')

    def test_func(self):
        artwork = self.get_object()
        return self.request.user == artwork.artist.user