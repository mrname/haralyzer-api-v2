from django.db import models
from django.utils.translation import gettext_lazy as _


class Scan(models.Model):
    """
    Represents a single "Scan" of a single URL.
    """
    class ScanStatus(models.TextChoices):
        # The scan has not started yet
        PENDING = 'pending', _('Pending')
        # The scan is currently running
        RUNNING = 'running', _('Running')
        # The scan has succeeded
        SUCCESS = 'success', _('Success')
        # The scan failed
        ERROR = 'error', _('Error')

    name = models.TextField()

    created = models.DateTimeField(auto_now_add=True, editable=False)

    # TODO - max length is only 200, should we up it?
    url = models.URLField()

    status = models.TextField(choices=ScanStatus.choices, default=ScanStatus.PENDING, editable=False)


class ScanResult(models.Model):
    scan = models.OneToOneField(
        Scan,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='result',
    )
    raw_results = models.JSONField()
