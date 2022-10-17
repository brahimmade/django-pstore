from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedUUIDModel


# Create your models here.
class Enquiry(TimeStampedUUIDModel):
    name = models.CharField(_("Your Name"), max_length=100)
    phone_number = PhoneNumberField(_("Phone Number"), default="+306900000000")
    email = models.CharField(_("Email"), max_length=100)
    subject = models.CharField(_("Subject"), max_length=100)
    message = models.CharField(_("Message"), max_length=255)

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name_plural = "Enqueries"
