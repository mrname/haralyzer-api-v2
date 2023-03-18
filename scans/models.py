from urllib.parse import urlparse

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

    # De-normalized from the URL for fast filtering
    hostname = models.TextField(editable=False)

    # TODO - Unused, but will be important when we move the scanning to
    # background task
    status = models.TextField(choices=ScanStatus.choices, default=ScanStatus.PENDING, editable=False)

    def save(self, *args, **kwargs):
        parsed_url = urlparse(self.url)
        self.hostname = parsed_url.hostname
        return super().save(*args, **kwargs)

class ScanResult(models.Model):
    # Attributes that are mapped directly from a HarPage to the model by name
    _haralyzer_defined_attrs = (
        'initial_load_time', 'html_load_time', 'image_load_time', 'css_load_time',
        'js_load_time', 'audio_load_time', 'video_load_time', 'image_size',
        'css_size', 'text_size', 'js_size', 'audio_size', 'video_size',
    )

    scan = models.OneToOneField(
        Scan,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='result',
    )

    # Store the raw results, so that we could "backfill" new properties in the
    # future if desired.
    raw_results = models.JSONField()

    # Store some denormalized data about the results. While we COULD calculate
    # such things dynamically at runtime, it makes sense to put them in the DB
    # to allow for fast user filtering
    total_load_time = models.IntegerField()
    initial_load_time = models.IntegerField()
    image_load_time = models.IntegerField()
    css_load_time = models.IntegerField()
    js_load_time = models.IntegerField()
    audio_load_time = models.IntegerField()
    video_load_time = models.IntegerField()
    html_load_time = models.IntegerField()

    total_size = models.IntegerField()
    image_size = models.IntegerField()
    css_size = models.IntegerField()
    text_size = models.IntegerField()
    js_size = models.IntegerField()
    audio_size = models.IntegerField()
    video_size = models.IntegerField()
