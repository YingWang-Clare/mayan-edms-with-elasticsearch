from __future__ import absolute_import, unicode_literals

from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from colorful.fields import RGBColorField

from acls.models import AccessControlList
from documents.models import Document
from documents.permissions import permission_document_view

from .events import event_tag_attach, event_tag_remove

from elasticsearch import Elasticsearch

@python_2_unicode_compatible
class Tag(models.Model):
    label = models.CharField(
        db_index=True, max_length=128, unique=True, verbose_name=_('Label')
    )
    color = RGBColorField(verbose_name=_('Color'))
    documents = models.ManyToManyField(
        Document, related_name='tags', verbose_name=_('Documents')
    )

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('tags:tag_tagged_item_list', args=(str(self.pk),))

    class Meta:
        ordering = ('label',)
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def attach_to(self, document, user=None):
        self.documents.add(document)
        event_tag_attach.commit(
            action_object=self, actor=user, target=document
        )
        self.add_tag_to_elasticsearch(document)

    def get_document_count(self, user):
        queryset = AccessControlList.objects.filter_by_access(
            permission_document_view, user, queryset=self.documents
        )

        return queryset.count()

    def remove_from(self, document, user=None):
        self.documents.remove(document)
        event_tag_remove.commit(
            action_object=self, actor=user, target=document
        )
        self.delete_tag_to_elasticsearch(document)

    # Todo: attach multiple tags to one document at one time
    def add_tag_to_elasticsearch(self, document):
        es, json_data = self.initialize_elasticsearch_and_data(document)
        json_id = str(json_data['hits']['hits'][0]['_id'])
        json_data['hits']['hits'][0]['_source']['tags__label'] += str(self.label + ';')
        es.update(index=settings.ELASTIC_SEARCH_INDEX, doc_type=settings.ELASTIC_SEARCH_DOC_TYPE, id=json_id, body={
            "doc": {
                "tags__label": json_data['hits']['hits'][0]['_source']['tags__label']
            }
        })

    def initialize_elasticsearch_and_data(self, document):
        es = Elasticsearch([{'host': settings.ELASTIC_SEARCH_HOST, 'port': settings.ELASTIC_SEARCH_PORT}])
        json_data = es.search(index=settings.ELASTIC_SEARCH_INDEX, body={
            "query": {
                "match": {
                    "uuid": document.uuid
                }
            }
        })
        return es, json_data

    def delete_tag_to_elasticsearch(self, document):
        es, json_data = self.initialize_elasticsearch_and_data(document)
        json_id = str(json_data['hits']['hits'][0]['_id'])
        es.update(index=settings.ELASTIC_SEARCH_INDEX, doc_type=settings.ELASTIC_SEARCH_DOC_TYPE, id=json_id, body={
            "doc": {
                "tags__label": json_data['hits']['hits'][0]['_source']['tags__label'].replace(str(self.label + ';'), '')
            }
        })


class DocumentTag(Tag):
    class Meta:
        proxy = True
        verbose_name = _('Document tag')
        verbose_name_plural = _('Document tags')
