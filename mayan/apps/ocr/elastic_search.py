from __future__ import absolute_import, unicode_literals
import logging
import json

from django.conf import settings

from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)

def initialize_es():
    logger.info('Initialize elastic search.')
    es = Elasticsearch([{'host': settings.ELASTIC_SEARCH_HOST, 'port': settings.ELASTIC_SEARCH_PORT}])
    return es

def construct_json_from_models(document_page, document_page_content):
    logger.info('Build a json object.')
    data = {}

    data['document_type__label'] = document_page.document.document_type.label
    data['versions__mimetype'] = document_page.document_version.mimetype
    data['label'] = document_page.document.label
    data['description'] = document_page.document.description
    data['versions__checksum'] = document_page.document_version.checksum
    data['cabinets__label'] = ''
    data['comments__comment'] = ''
    data['versions__pages__content__content'] = document_page_content.content
    data['metadata__metadata_type__name'] = ''
    data['metadata__value'] = ''
    data['versions__pages__ocr_content__content'] = document_page_content.content
    data['tags__label'] = ''

    data['versions__pages__page_number'] = document_page.page_number
    data['versions__pages__uuid'] = document_page.uuid
    data['versions__pages__pk'] = document_page.pk
    data['versions__version'] = document_page.document_version.__str__()
    data['versions__timestamp'] = str(document_page.document_version.timestamp)
    data['uuid'] = str(document_page.document_version.document.uuid)
    data['pk'] = document_page.document_version.document.pk

    # print('data: ', data)
    json_data = json.dumps(data)
    # print('json: ', json_data)
    return json_data

def insert_into_es(es, json_data):
    es.index(index=settings.ELASTIC_SEARCH_INDEX, doc_type=settings.ELASTIC_SEARCH_DOC_TYPE, body=json_data)
    logger.info('Inserted a json data to elastic search.')