from django.contrib.auth import get_user_model
from django.db.models import signals as signal
from django.dispatch import receiver

from game_hub.accounts.models import Profile

UserModel = get_user_model()


@receiver(signal.post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(
            user=instance
        )
        profile.save()




