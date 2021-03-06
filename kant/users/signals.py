from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DomesticNewsModel
from fcm_django.models import FCMDevice


@receiver(post_save, sender=DomesticNewsModel)
def send_fcm_notification(sender, instance, **kwargs):
    # FCMDevice.objects.create(registration_id=233,device_id=)
    devices = FCMDevice.objects.all()
    if len(devices) > 0:
        body = str(instance.content) + "\n" + str(instance.description)
        devices.send_message(title=instance.name, body=body, sound='Default')
        print("sending message ... ")
    return
