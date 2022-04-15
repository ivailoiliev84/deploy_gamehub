from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from game_hub.accounts.models import Profile
from game_hub.core.forms_bootstrap import BootstrapFormMixin

UserModel = get_user_model()


class CreateGameHubUser(UserCreationForm):
    bot_catcher = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def clean_bot_catcher(self):
        bot_catcher = self.cleaned_data['bot_catcher']
        if bot_catcher:
            raise forms.ValidationError('Bot detected')

    class Meta:
        model = UserModel
        fields = ('email',)


class LoginForm(AuthenticationForm):
    pass


class CreateProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

        widgets = {
            'profile_picture': forms.FileInput()
        }
