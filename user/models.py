from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth import get_user_model


class Department(models.Model):
    name = models.CharField(u'部门', max_length=32, null=True)
    parent = models.ForeignKey('self', verbose_name='上级部门', null=True, blank=True, related_name='child',
                               on_delete=models.CASCADE)
    admins = models.ManyToManyField(to='UserProfile', verbose_name="管理员", blank=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = u'部门管理'
        verbose_name_plural = u'部门管理'


class Role(models.Model):
    name = models.CharField(u'职位', max_length=32, null=True)
    permissions = models.ManyToManyField(to=Permission, verbose_name="权限组", blank=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = u'职位管理'
        verbose_name_plural = u'职位管理'


@receiver(post_save, sender=Role)
def sync_auth(sender, instance=None, created=False, **kwargs):
    user_model = get_user_model()
    users = user_model.objects.all().filter(role=instance)
    for user in users:
        role_list = user.role.all()
        user_permissions_set = {permissions for role in role_list for permissions in role.permissions.all()}
        user.user_permissions.clear()
        user.user_permissions.add(*user_permissions_set)
        user.save()


class UserProfile(AbstractUser):
    mobile = models.CharField(u'手机', max_length=11, null=True)
    role = models.ManyToManyField('Role', verbose_name='职位', blank=True)
    dept = models.ForeignKey(Department, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "%s%s" % (self.last_name, self.first_name)

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        if self.role is not None:
            role_list = self.role.all()
            user_permissions_set = {permissions for role in role_list for permissions in role.permissions.all()}
            self.user_permissions.clear()
            self.user_permissions.add(*user_permissions_set)
            super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'用户管理'
        verbose_name_plural = u'用户管理'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
