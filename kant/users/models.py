from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from decouple import config
from django.db.models.signals import (
    post_save,
    post_delete,
)


class AbstractDateTimeModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class UserProfile(AbstractDateTimeModel):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField("Телефон", max_length=50)
    email = models.EmailField("Почта", max_length=50)
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    fathers_name = models.CharField("Отчество", max_length=50, null=True, blank=True)
    date_of_birth = models.DateField("Дата рождения", null=False, default=timezone.now)
    list_phones = ArrayField(base_field=models.CharField(
        max_length=30, null=True, blank=True),
        size=6, max_length=(6 * 31), null=True, blank=True)
    address = models.CharField("Адрес", max_length=50, null=False)
    city = models.CharField("Город", max_length=50, null=True, blank=True)
    photo = models.CharField("Фото пользователя", max_length=1000, null=True, blank=True)
    firebase_token = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.user.username + " id: " + str(self.user.id)


class DomesticNewsModel(AbstractDateTimeModel):
    name = models.CharField(max_length=500, null=True, verbose_name='Название')
    description = models.TextField(null=True, verbose_name='Описание')
    content = models.TextField(null=True, verbose_name='Контент')

    class Meta:
        verbose_name = "Местная Новость"
        verbose_name_plural = "Местные Новости"

    def __str__(self):
        return "{}. {}".format(self.pk, self.name)

    def __repr__(self):
        return "{}. {}".format(self.pk, self.name)


class DomesticNewsPhotoLink(models.Model):
    domestic = models.ForeignKey(DomesticNewsModel,
                                 on_delete=models.CASCADE,
                                 verbose_name='Местная новость')
    photo_link = models.CharField(max_length=500, blank=True, null=True, verbose_name='Ссылка на фото')

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"


# def send_firebase_message(sender, instance, created, *args, **kwargs):
#     if created:
#         import json
#         import requests
#         tokens = UserProfile.objects.values_list('firebase_token')
#         params = {}
#         params['title'] = instance.name
#         params['sound'] = "default"
#         values = {
#             'content-available': True,
#             'priority': 'high',
#             # 'to': '/topics/domestic_news',
#             "registration_ids": [item[0] for item in tokens],
#             'notification': params
#         }
#
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': 'key=' + config('FCM_API')
#         }
#
#         requests.post(url="https://fcm.googleapis.com/fcm/send", data=json.dumps(values), headers=headers)
#
#
# post_save.connect(send_firebase_message, sender=DomesticNewsModel)