from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from dynamic_search.classes import SearchModel

from .permissions import permission_document_view

# Search Model for document search
document_search = SearchModel(
    app_label='documents', model_name='Document',
    permission=permission_document_view,
    serializer_string='documents.serializers.DocumentSerializer'
)

document_search.add_model_field(
    field='document_type__label', label=_('Document type')
)
document_search.add_model_field(
    field='versions__mimetype', label=_('MIME type')
)
document_search.add_model_field(field='label', label=_('Label'))
document_search.add_model_field(field='description', label=_('Description'))
document_search.add_model_field(
    field='versions__checksum', label=_('Checksum')
)

# Search Model for document page search

document_page_search = SearchModel(
    app_label='documents', model_name='DocumentPageResult',
    permission=permission_document_view,
    serializer_string='documents.serializers.DocumentPageSerializer'
)
# In classes.py search(), the field should be the attributes of DocumentPage Model, since the result will be
# obtained from the DocumentPageManager's filter() method. But in classes.py elastic_search(), we need to find all
# result from elasticsearch, so the field's name should be the same as the field in elasticsearch.

# document_page_search.add_model_field(
#     field='document_version__document__document_type__label',
#     label=_('Document type')
# )
# document_page_search.add_model_field(
#     field='document_version__document__versions__mimetype',
#     label=_('MIME type')
# )
# document_page_search.add_model_field(
#     field='document_version__document__label', label=_('Label')
# )
# document_page_search.add_model_field(
#     field='document_version__document__description', label=_('Description')
# )
# document_page_search.add_model_field(
#     field='document_version__checksum', label=_('Checksum')
# )


document_page_search.add_model_field(
    field='document_type__label',
    label=_('Document type')
)
document_page_search.add_model_field(
    field='versions__mimetype',
    label=_('MIME type')
)
document_page_search.add_model_field(
    field='label', label=_('Label')
)
document_page_search.add_model_field(
    field='description', label=_('Description')
)
document_page_search.add_model_field(
    field='versions__checksum', label=_('Checksum')
)

