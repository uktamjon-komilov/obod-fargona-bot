from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    class Meta:
        verbose_name = "Telegram profil"
        verbose_name_plural = "Telegram profillar"

    tg_id = models.CharField(max_length=16, unique=True, verbose_name="ID")
    tg_username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telegram nomi (@username)")
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ismi")
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Familiyasi")
    step = models.CharField(max_length=255, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tg_id or ""


class Appeal(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=255)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    comment = models.TextField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)

    google_maps_url = models.TextField()

    def __str__(self):
        return self.phone


class Photo(models.Model):
    photo = models.ImageField()
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)