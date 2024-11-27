from django.db import models
from artworks.models import Artwork

class Exhibition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    artworks = models.ManyToManyField(Artwork)
    location = models.CharField(max_length=200)  # Add this line
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title