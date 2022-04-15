from django.urls import path

from game_hub.information.views import ContactView

urlpatterns = (
    path('contacts/', ContactView.as_view(), name='contacts'),
)
