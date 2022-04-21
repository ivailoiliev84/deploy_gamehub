from django.urls import path
from django.contrib.auth import views as auth_views

# from game_hub.accounts.views import RegisterUser, logout_user, ProfilePageView, \
#     LoginUserView, ChangePasswordView, ProfileEditView, ProfileDeleteView
from game_hub.accounts.views import *

urlpatterns = (
    path('register/', RegisterUser.as_view(), name='register'),
    path('log-in/', LoginUserView.as_view(), name='login'),
    path('log-out/', logout_user, name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change password'),

    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('profile-edit/<int:pk>', ProfileEditView.as_view(), name='profile edit'),
    path('profile-delte/<int:pk>', ProfileDeleteView.as_view(), name='profile delete'),



    # path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complate/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

)

from .signals_accounts import *