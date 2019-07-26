from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from actstream.models import Action

from .classes import EventType
from .managers import (
    EventSubscriptionManager, ObjectEventSubscriptionManager
)


@python_2_unicode_compatible
class StoredEventType(models.Model):
    name = models.CharField(
        max_length=64, unique=True, verbose_name=_('Name')
    )

    class Meta:
        verbose_name = _('Stored event type')
        verbose_name_plural = _('Stored event types')

    def __str__(self):
        return force_text(self.get_class())

    def get_class(self):
        return EventType.get(name=self.name)

    @property
    def label(self):
        return self.get_class().label

    @property
    def namespace(self):
        return self.get_class().namespace


@python_2_unicode_compatible
class EventSubscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, db_index=True, on_delete=models.CASCADE,
        related_name='event_subscriptions', verbose_name=_('User')
    )
    stored_event_type = models.ForeignKey(
        StoredEventType, on_delete=models.CASCADE,
        related_name='event_subscriptions', verbose_name=_('Event type')
    )

    objects = EventSubscriptionManager()

    class Meta:
        verbose_name = _('Event subscription')
        verbose_name_plural = _('Event subscriptions')

    def __str__(self):
        return force_text(self.stored_event_type)


@python_2_unicode_compatible
class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, db_index=True, on_delete=models.CASCADE,
        related_name='notifications', verbose_name=_('User')
    )
    action = models.ForeignKey(
        Action, on_delete=models.CASCADE, related_name='notifications',
        verbose_name=_('Action')
    )
    read = models.BooleanField(default=False, verbose_name=_('Read'))

    class Meta:
        ordering = ('-action__timestamp',)
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return force_text(self.action)


@python_2_unicode_compatible
class ObjectEventSubscription(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, db_index=True, on_delete=models.CASCADE,
        related_name='object_subscriptions', verbose_name=_('User')
    )
    stored_event_type = models.ForeignKey(
        StoredEventType, on_delete=models.CASCADE,
        related_name='object_subscriptions', verbose_name=_('Event type')
    )

    objects = ObjectEventSubscriptionManager()

    class Meta:
        verbose_name = _('Object event subscription')
        verbose_name_plural = _('Object event subscriptions')

    def __str__(self):
        return force_text(self.stored_event_type)
