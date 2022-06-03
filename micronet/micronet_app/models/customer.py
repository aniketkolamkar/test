from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parentUsername = models.CharField(max_length=100)
    emailConfirmed = models.BooleanField(default=False)
    reset_password = models.BooleanField(default=False)
    address = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=10,default="0")
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "'butler@6simplex.co.in",
        # to:
        [reset_password_token.user.email]
    )

    # send_mail(
    #         'subject', 
    #         'body of the message', 
    #         'butler@6simplex.co.in', 
    #         [
    #             'aniketkolamkar@6simplex.co.in'
    #         ]
    #     ) 