from __future__ import unicode_literals

import logging

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from documents.models import Document

from .events import (
    event_document_comment_create, event_document_comment_delete
)
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Comment(models.Model):
    document = models.ForeignKey(
        Document, db_index=True, on_delete=models.CASCADE,
        related_name='comments', verbose_name=_('Document')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=False, on_delete=models.CASCADE,
        related_name='comments', verbose_name=_('User'),
    )
    # Translators: Comment here is a noun and refers to the actual text stored
    comment = models.TextField(verbose_name=_('Comment'))
    submit_date = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name=_('Date time submitted')
    )

    def __str__(self):
        return self.comment

    def save(self, *args, **kwargs):
        user = kwargs.pop('_user', None) or self.user
        is_new = not self.pk
        super(Comment, self).save(*args, **kwargs)
        if is_new:
            if user:
                event_document_comment_create.commit(
                    actor=user, target=self.document
                )
                logger.info(
                    'Comment "%s" added to document "%s" by user "%s"',
                    self.comment, self.document, user
                )
            else:
                event_document_comment_create.commit(target=self.document)
                logger.info(
                    'Comment "%s" added to document "%s"', self.comment,
                    self.document
                )
            self.add_comment_to_elasticsearch()

    def delete(self, *args, **kwargs):
        user = kwargs.pop('_user', None)
        super(Comment, self).delete(*args, **kwargs)
        if user:
            event_document_comment_delete.commit(
                actor=user, target=self.document
            )
        else:
            event_document_comment_delete.commit(target=self.document)
        self.delete_comment_to_elasticsearch()

    def add_comment_to_elasticsearch(self):
        es, json_data = self.initialize_elasticsearch_and_data()
        json_id = str(json_data['hits']['hits'][0]['_id'])
        json_data['hits']['hits'][0]['_source']['comments__comment'] += str(self.comment + ';')
        logger.info('Comment update complete.')
        es.update(index=settings.ELASTIC_SEARCH_INDEX, doc_type=settings.ELASTIC_SEARCH_DOC_TYPE, id=json_id, body={
            "doc": {
                "comments__comment": json_data['hits']['hits'][0]['_source']['comments__comment']
            }
        })
        logger.info('Update the updated doc into ES.')

    def initialize_elasticsearch_and_data(self):
        logger.info('Load ES.')
        es = Elasticsearch([{'host': settings.ELASTIC_SEARCH_HOST, 'port': settings.ELASTIC_SEARCH_PORT}])
        json_data = es.search(index=settings.ELASTIC_SEARCH_INDEX, body={
            "query": {
                "match": {
                    "uuid": self.document.uuid
                }
            }
        })
        return es, json_data

    def delete_comment_to_elasticsearch(self):
        es, json_data = self.initialize_elasticsearch_and_data()
        json_id = str(json_data['hits']['hits'][0]['_id'])
        es.update(index=settings.ELASTIC_SEARCH_INDEX, doc_type=settings.ELASTIC_SEARCH_DOC_TYPE, id=json_id, body={
            "doc": {
                "comments__comment": json_data['hits']['hits'][0]['_source']['comments__comment'].replace(str(self.comment + ';'), '')
            }
        })
        logger.info('Update the updated doc into ES.')

    class Meta:
        get_latest_by = 'submit_date'
        ordering = ('-submit_date',)
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
