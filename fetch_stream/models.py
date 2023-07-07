import datetime
from enum import Enum, IntEnum, unique

from django.contrib.postgres.fields import JSONField
from django.db import models


@unique
class StreamMessageStatus(IntEnum):
    PENDING = 1
    FETCHED = 2
    DELETED = 3
    UPDATED = 4

@unique
class StreamMessageAction(Enum):
    ADD = 'add'
    UPDATE = 'rep'
    DELETE = 'del'


class Account(models.Model):
    """
    contains details related to subscribed stream account
    """
    name = models.CharField(max_length=75)
    user_key = models.CharField(max_length=75, db_index=True, unique=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=True, db_index=True)
    updated_on = models.DateTimeField(db_index=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated_on = datetime.datetime.now()
        return super(Account, self).save(*args, **kwargs)


class Stream(models.Model):
    """
    contains details related to subscribed stream
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=75)
    stream_id = models.CharField(
        max_length=100, db_index=True, unique=True
    )
    subscription_id = models.CharField(
        max_length=100, db_index=True, unique=True,
        null=True  # should be a required field
    )
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=True, db_index=True)
    updated_on = models.DateTimeField(db_index=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name}: {self.stream_id}'

    def save(self, *args, **kwargs):
        self.updated_on = datetime.datetime.now()
        return super(Stream, self).save(*args, **kwargs)


class StreamMessage(models.Model):
    """
    model class to manage messages/data received from stream source/pipeline
    """
    stream = models.ForeignKey(
        Stream, db_index=True, on_delete=models.CASCADE
    )
    message_id = models.CharField(max_length=100)
    raw_message_dict = JSONField(
        default=None, null=True, blank=True,
        help_text='contains data received from stream'
    )
    status = models.IntegerField(
        db_index=True,
        choices=[(item.value, item.name) for item in StreamMessageStatus],
        default=StreamMessageStatus.PENDING.value
    )
    action = models.CharField(
        db_index=True, max_length=5,
        choices=[(item.value, item.name) for item in StreamMessageAction],
        default=StreamMessageAction.ADD.value
    )
    created_on = models.DateTimeField(auto_now=True, db_index=True)
    updated_on = models.DateTimeField(db_index=True, null=True, blank=True)

    class Meta:
        unique_together = ('message_id', 'action')

    def __str__(self):
        return f'{self.message_id}: {self.action}'

    def save(self, *args, **kwargs):
        self.updated_on = datetime.datetime.now()
        return super(StreamMessage, self).save(*args, **kwargs)
