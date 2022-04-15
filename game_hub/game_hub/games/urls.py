from django.urls import path

from game_hub.games.views import HomeView, CatalogueListView, \
    create_comment, GameMyGames, create_like, GameCreateView, GameDetailsView, GameEditView, DeleteGameView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('catalogue/', CatalogueListView.as_view(), name='catalogue list'),
    path('create-game/', GameCreateView.as_view(), name='create game'),
    path('details/<int:pk>', GameDetailsView.as_view(), name='game details'),
    path('edit/<int:pk>', GameEditView.as_view(), name='game edit'),
    path('delete/<int:pk>', DeleteGameView.as_view(), name='delete game'),
    path('game/my-games', GameMyGames.as_view(), name='my games'),


    path('comment/<int:pk>', create_comment, name='create comment'),
    path('like-game/<int:pk>', create_like, name='like game'),

)
