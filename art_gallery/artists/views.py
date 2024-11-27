from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Artist
from artworks.models import Artwork
from exhibitions.models import Exhibition

class ArtistListView(ListView):
    model = Artist
    template_name = 'artists/artist_list.html'
    context_object_name = 'artists'
    paginate_by = 12

    def get_queryset(self):
        queryset = Artist.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(bio__icontains=search_query)
            )
        return queryset

class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'artists/artist_detail.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist = self.get_object()
        context['artworks'] = artist.artwork_set.all().order_by('-created_at')
        context['exhibitions'] = Exhibition.objects.filter(artworks__artist=artist).distinct()
        context['featured_artwork'] = artist.artwork_set.filter(is_featured=True).first()
        return context

class ArtistCreateView(LoginRequiredMixin, CreateView):
    model = Artist
    template_name = 'artists/artist_form.html'
    fields = ['bio', 'contact', 'website']
    success_url = reverse_lazy('artist-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ArtistUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Artist
    template_name = 'artists/artist_form.html'
    fields = ['bio', 'contact', 'website']

    def test_func(self):
        artist = self.get_object()
        return self.request.user == artist.user

    def get_success_url(self):
        return reverse_lazy('artist-detail', kwargs={'pk': self.object.pk})

class ArtistDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Artist
    template_name = 'artists/artist_confirm_delete.html'
    success_url = reverse_lazy('artist-list')

    def test_func(self):
        artist = self.get_object()
        return self.request.user == artist.user

# Additional views for artist portfolio management
class ArtistPortfolioView(DetailView):
    model = Artist
    template_name = 'artists/artist_portfolio.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist = self.get_object()
        context['artworks'] = artist.artwork_set.all().order_by('-created_at')
        context['exhibitions'] = Exhibition.objects.filter(
            artworks__artist=artist
        ).distinct().order_by('-start_date')
        context['artwork_count'] = context['artworks'].count()
        context['exhibition_count'] = context['exhibitions'].count()
        return context
    
    