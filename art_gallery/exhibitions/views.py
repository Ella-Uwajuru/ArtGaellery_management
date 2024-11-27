from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Exhibition
from .forms import ExhibitionForm

class ExhibitionListView(ListView):
    model = Exhibition
    template_name = 'exhibitions/exhibition_list.html'
    context_object_name = 'exhibitions'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Exhibition.objects.all().order_by('-start_date')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Status filter
        status = self.request.GET.get('status')
        today = timezone.now().date()
        if status == 'upcoming':
            queryset = queryset.filter(start_date__gt=today)
        elif status == 'ongoing':
            queryset = queryset.filter(start_date__lte=today, end_date__gte=today)
        elif status == 'past':
            queryset = queryset.filter(end_date__lt=today)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context


class ExhibitionDetailView(DetailView):
    model = Exhibition
    template_name = 'exhibitions/exhibition_detail.html'
    context_object_name = 'exhibition'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exhibition = self.get_object()
        
        # Add related exhibitions
        context['related_exhibitions'] = Exhibition.objects.filter(
            Q(curator=exhibition.curator) | 
            Q(artworks__artist__in=[artwork.artist for artwork in exhibition.artworks.all()])
        ).exclude(id=exhibition.id).distinct()[:3]
        
        return context


class ExhibitionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Exhibition
    form_class = ExhibitionForm
    template_name = 'exhibitions/exhibition_form.html'
    success_url = reverse_lazy('exhibition-list')

    def test_func(self):
        return self.request.user.is_artist

    def form_valid(self, form):
        form.instance.curator = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ExhibitionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Exhibition
    form_class = ExhibitionForm
    template_name = 'exhibitions/exhibition_form.html'

    def test_func(self):
        exhibition = self.get_object()
        return self.request.user == exhibition.curator

    def get_success_url(self):
        return reverse_lazy('exhibition-detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ExhibitionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Exhibition
    template_name = 'exhibitions/exhibition_confirm_delete.html'
    success_url = reverse_lazy('exhibition-list')

    def test_func(self):
        exhibition = self.get_object()
        return self.request.user == exhibition.curator


# Additional view for managing artworks in an exhibition
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def manage_exhibition_artwork(request, exhibition_id):
    exhibition = get_object_or_404(Exhibition, id=exhibition_id, curator=request.user)
    artwork_id = request.POST.get('artwork_id')
    action = request.POST.get('action')
    
    if action == 'add':
        exhibition.artworks.add(artwork_id)
        message = 'Artwork added to exhibition'
    elif action == 'remove':
        exhibition.artworks.remove(artwork_id)
        message = 'Artwork removed from exhibition'
    
    return JsonResponse({'status': 'success', 'message': message})