import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views import generic as view

# Create your views here.
from game_hub.games.forms import GameForm, CommentForm
from game_hub.games.models import Game, Comment, LikeGame


class HomeView(view.TemplateView):
    template_name = 'base/home_page.html'


class CatalogueListView(LoginRequiredMixin, view.ListView):
    template_name = 'game_templates/game_catalogue.html'
    model = Game
    context_object_name = 'games'
    paginate_by = 3


class GameCreateView(LoginRequiredMixin, view.FormView):
    form_class = GameForm
    template_name = 'game_templates/game_create.html'
    success_url = reverse_lazy('catalogue list')

    def form_valid(self, form):
        game = form.save(commit=False)
        game.user = self.request.user
        game.save()
        return super().form_valid(form)


class GameDetailsView(LoginRequiredMixin, view.DetailView):
    model = Game
    template_name = 'game_templates/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = context['game']

        context['form'] = CommentForm
        context['game'] = game
        context['is_owner'] = game.user == self.request.user
        context['comments'] = game.comment_set.all()
        context['user'] = self.request.user
        context['like_game_count'] = game.likegame_set.all().count()

        return context


class GameEditView(LoginRequiredMixin, view.UpdateView):
    model = Game
    template_name = 'game_templates/game_edit.html'
    form_class = GameForm
    success_url = reverse_lazy('my games')
    context_object_name = 'game'


class DeleteGameView(LoginRequiredMixin, view.DeleteView):
    template_name = 'game_templates/game_delete.html'
    model = Game
    success_url = reverse_lazy('my games')
    context_object_name = 'game'

    """
    problem  ->  if user  don't confirm operation delete, delete view find and delete game image!!! This is  bug!!! 
    waiting for  resolve problem!
    """

    # def get_context_data(self, **kwargs):
    #     context = super(DeleteGameView, self).get_context_data(**kwargs)
    #     game = context['game']
    #     old_image = game.image.path
    #     os.remove(old_image)
    #     return context


class GameMyGames(LoginRequiredMixin, view.ListView):
    template_name = 'game_templates/game_my_games.html'
    model = Game
    context_object_name = 'games'
    paginate_by = 3

    def get_queryset(self):
        games = Game.objects.filter(user_id=self.request.user.id)
        return games


def create_comment(request, pk):
    game = Game.objects.get(pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = Comment(
            comment=form.cleaned_data['comment'],
            game=game,
            user=request.user,
        )
        comment.save()
        return redirect('game details', game.id)


def create_like(request, pk):
    game = Game.objects.get(pk=pk)
    user_who_like = game.likegame_set.filter(user_id=request.user.id).first()

    if user_who_like:
        user_who_like.delete()
    else:
        like = LikeGame(
            game=game,
            user=request.user,
        )
        like.save()
    return redirect('game details', game.id)
