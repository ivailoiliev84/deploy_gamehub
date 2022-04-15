from django.urls import path

from game_hub.accounts.views import RegisterUser, logout_user, ProfilePageView, \
    LoginUserView, ChangePasswordView, ProfileEditView, ProfileDeleteView

urlpatterns = (
    path('register/', RegisterUser.as_view(), name='register'),
    path('log-in/', LoginUserView.as_view(), name='login'),
    path('log-out/', logout_user, name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change password'),

    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('profile-edit/<int:pk>', ProfileEditView.as_view(), name='profile edit'),
    path('profile-delte/<int:pk>', ProfileDeleteView.as_view(), name='profile delete')
)
