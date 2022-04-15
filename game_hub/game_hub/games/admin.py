from django.contrib import admin


# Register your models here.
from game_hub.games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'max_level',)
