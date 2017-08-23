from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset()

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=100, default='', verbose_name="Город")
    phone = models.IntegerField(default=0, verbose_name="Телефон")
    position = models.CharField(max_length=100, default='', verbose_name="Должность")
    image = models.ImageField(upload_to='profile_image', blank=True, verbose_name="Фото")

    n = UserProfileManager()
    objects = models.Manager()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = UserProfile.objects.create(user=kwargs['instance'])
#
# post_save.connect(create_profile, sender=User)