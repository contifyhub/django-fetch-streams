import datetime
from enum import Enum, IntEnum, unique

from django.contrib.postgres.fields import JSONField
from django.db import models


@unique
class StreamDataStatus(IntEnum):
    PENDING = 1
    FETCHED = 2


@unique
class StreamDataAction(Enum):
    ADD = 'add'
    UPDATE = 'rep'
    DELETE = 'del'


class DnaStream(models.Model):
    """
    contains details related to subscribed stream
    """
    name = models.CharField(max_length=75)
    stream_id = models.CharField(max_length=100, db_index=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=True, db_index=True)
    updated_on = models.DateTimeField(db_index=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name}: {self.stream_id}'

    def save(self, *args, **kwargs):
        self.updated_on = datetime.datetime.now()
        return super(DnaStream, self).save(*args, **kwargs)


class StreamData(models.Model):
    """
    model class to manage stream data fetched from stream source
    """
    stream_id = models.ForeignKey(
        DnaStream, db_index=True, on_delete=models.CASCADE
    )
    data_id = models.CharField(max_length=100, unique=True)
    raw_data_dict = JSONField(
        default=None, null=True, blank=True,
        help_text='contains data received from stream'
    )
    status = models.IntegerField(
        db_index=True,
        choices=[(item.value, item.name) for item in StreamDataStatus],
        default=StreamDataStatus.PENDING.value
    )
    action = models.CharField(
        db_index=True, max_length=5,
        choices=[(item.value, item.name) for item in StreamDataAction],
        default=StreamDataAction.ADD.value
    )
    created_on = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        unique_together = ('data_id', 'action')

    def __str__(self):
        return f'{self.data_id}: {self.action}'
