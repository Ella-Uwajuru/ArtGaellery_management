from django.shortcuts import render
from django.db.models import Count
from artists.models import Artist
from artworks.models import Artwork
from exhibitions.models import Exhibition

def home(request):
    # Count the number of artists, artworks, and exhibitions
    artist_count = Artist.objects.count()
    artwork_count = Artwork.objects.count()
    exhibition_count = Exhibition.objects.count()

    context = {
        'data_labels': ['Artists', 'Artworks', 'Exhibitions'],
        'data_counts': [artist_count, artwork_count, exhibition_count],
    }
    return render(request, 'home.html', context)