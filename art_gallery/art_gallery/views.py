from django.shortcuts import render
from artists.models import Artist
from django.db.models import Count

def home(request):
    # Get all artists with their artwork counts only
    artists_data = Artist.objects.annotate(
        artwork_count=Count('artwork', distinct=True)
    ).values('user__first_name', 'artwork_count')
    
    # Prepare data for the chart
    artist_names = [artist['user__first_name'] for artist in artists_data]
    artwork_counts = [artist['artwork_count'] for artist in artists_data]
    
    context = {
        'artist_names': artist_names,
        'artwork_counts': artwork_counts,
        'exhibition_counts': [0] * len(artist_names),  # Temporary placeholder
    }
    return render(request, 'home.html', context)