from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


UserModel = get_user_model()


@shared_task
def send_emial_on_new_user(user_pk):
    user = UserModel.objects.get(pk=user_pk)
    send_mail(
            'Wewcome',
            'Hello from us',
            'gamehub.test.heroku@gmail.com',
            (user.email,),
        )