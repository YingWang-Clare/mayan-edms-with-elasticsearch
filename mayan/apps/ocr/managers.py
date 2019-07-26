from __future__ import unicode_literals

import logging
import sys
import traceback

from django.apps import apps
from django.conf import settings
from django.db import models

from documents.runtime import cache_storage_backend

from .events import event_ocr_document_version_finish
from .runtime import ocr_backend
from .signals import post_document_version_ocr

from .elastic_search import initialize_es, insert_into_es, construct_json_from_models

logger = logging.getLogger(__name__)


class DocumentPageOCRContentManager(models.Manager):
    def process_document_version(self, document_version):
        logger.info('Starting OCR for document version: %s', document_version)
        logger.debug('document version: %d', document_version.pk)

        try:
            # init es
            es = initialize_es()
            for document_page in document_version.pages.all():
                self.process_document_page(document_page=document_page, es=es)
        except Exception as exception:
            logger.error(
                'OCR error for document version: %s; %s', document_version,
                exception
            )

            if settings.DEBUG:
                result = []
                type, value, tb = sys.exc_info()
                result.append('%s: %s' % (type.__name__, value))
                result.extend(traceback.format_tb(tb))
                document_version.ocr_errors.create(
                    result='\n'.join(result)
                )
            else:
                document_version.ocr_errors.create(result=exception)
        else:
            logger.info(
                'OCR complete for document version: %s', document_version
            )
            document_version.ocr_errors.all().delete()

            event_ocr_document_version_finish.commit(
                action_object=document_version.document,
                target=document_version
            )

            post_document_version_ocr.send(
                sender=document_version.__class__, instance=document_version
            )

    def process_document_page(self, document_page, es):
        logger.info(
            'Processing page: %d of document version: %s',
            document_page.page_number, document_page.document_version
        )

        DocumentPageOCRContent = apps.get_model(
            app_label='ocr', model_name='DocumentPageOCRContent'
        )

        # TODO: Call task and wait
        cache_filename = document_page.generate_image()

        with cache_storage_backend.open(cache_filename) as file_object:
            document_page_content, created = DocumentPageOCRContent.objects.get_or_create(
                document_page=document_page
            )
            document_page_content.content = ocr_backend.execute(
                file_object=file_object,
                language=document_page.document.language
            )
            logger.info(
                'Finished processing page: %d of document version: %s',
                document_page.page_number, document_page.document_version
            )
            document_page_content.save()

            logger.info(
                'Start to process with ElasticSearch for page: %d of document version: %s',
                document_page.page_number, document_page.document_version
            )
            # # create json data
            json_data = construct_json_from_models(document_page, document_page_content)
            # # insert into es
            insert_into_es(es=es, json_data=json_data)



