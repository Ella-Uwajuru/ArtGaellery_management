from django.contrib import admin
from .models import Artist

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact', 'website', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio')
    list_filter = ('created_at',)