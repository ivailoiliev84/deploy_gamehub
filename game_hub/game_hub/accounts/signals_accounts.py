from django.contrib.auth import get_user_model
from django.db.models import signals as signal
from django.dispatch import receiver

from game_hub.accounts.models import Profile
from game_hub.accounts.tasks import *

UserModel = get_user_model()


@receiver(signal.post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(
            user=instance
        )
        profile.save()




# @receiver(signal.post_save, sender=UserModel)
# def send_email_when_user_is_create(sender, instance, created, **kwargs):
#     if created:
#         send_emial_on_new_user.delay(instance.pk)