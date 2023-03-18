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

    # TODO - It doesn't really NEED to be a file. We could always just store it
    # in a JSON blob as well (its just a JSON file). Using file based storage
    # for now to keep the database trim, and also allow users a downloadable
    # URL as a feature
    har_file = models.FileField(editable=False)

    # The rest of the scan stuff will be dynamically generated (probably in the
    # serializer) using haralyzer. Technically, we might want to store some of
    # this data directly into the DB as well for faster searching/filtering
    # (like storing the total load time for example, allowing users to search
    # for scans that took over X MS).
