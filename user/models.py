from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save, post_delete


class UserProfile(AbstractUser):
    mobile = models.CharField(u'手机', max_length=11, null=True)

    def __str__(self):
        return "%s%s" % (self.last_name, self.first_name)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
