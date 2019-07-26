=======
Roadmap
=======

- Workflow:

  - Improve workflow system
  - Workflow actions. Predefined actions to be execute on document leaving or entering a state or a transition. Example: "Add to folder X", "Attach tag X".
  - Add support for state recipients.
  - Add workflow document inbox notification.

- Indexing

  - Replace indexing and smart linking template language (use Jinja2 instead of Django's).

- Distribution:

  - Debian packages. Limited success so far using https://github.com/astraw/stdeb.

- Notifications:

  - Add support for subscribing to a document's events.
  - Add support for subscribing to a document type events.
  - Add support for subscribing specific events.

- OCR:

  - Add image preprocessing for OCR. Increase effectiveness of Tesseract.

- Python 3:

  - Complete support for Python3.
  - Find replacement for pdfminer (Python3 support blocker). Use pdfminer.six (#257).

- Simple serving:

  - Provide option to serve Mayan EDMS without a webserver (using Tornado o similar). Work started in branch: ``/feature/tornado``

- Upload wizard:

  - Make wizard step configurable. Create ``WirzardStep`` class so apps can add their own upload wizard steps, instead of the steps being hardcoded in the sources app.
  - Add upload wizard step to add the new documents to a folder.

- Other

  - Use a sequence and not the document upload date to determine the document version sequence. MySQL doesn't store milisecond value in dates and if several version are uploaded in a single second there is no way to know the order or which one is the latests. This is why the document version tests include a 2 second delay. Possible solution: http://schinckel.net/2015/05/17/django-second-autofield/
  - Include external app Mayan-EXIF into main code.
  - Convert all views from functions to class based views (CBV).
  - Increase test coverage.
  - Mock external services in tests. For example the ``django_GPG`` app key search and receive tests.
  - Pluggable icon app. Make switching icon set easier.
  - Reduce dependency on binary executables for a default install.
  - Find replacement for ``cssmin`` & ``django-compressor``.
  - Find replacement for ``python-gnupg``. Unstable & inconsistent API.
  - Google docs integration. Upload document from Google Drive.
  - Get ``dumpdata`` and ``loaddata`` working flawlessly. Will allow for easier backups, restores and database backend migrations.
  - Add generic list ordering. ``django.views.generic.list.MultipleObjectMixin`` (https://docs.djangoproject.com/en/1.8/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin) now supports an ``ordering`` parameter.
  - Add support to convert any document to PDF. https://gitlab.mister-muffin.de/josch/img2pdf
  - Add support for combining documents.
  - Add support for splitting documents.
  - Add new document source to get documents from an URL.
  - Document overlay support. Such as watermarks. https://gist.github.com/umrashrf/8616550
  - Add support for metadata mapping files. CSV file containing filename to metadata values mapping, useful for bulk upload and migrations.
  - Add support for registering widgets to the home screen.
  - Merge mimetype and converter apps.
  - Add GPG key generation.
  - If SourceColumn label is None take description from model. Avoid unnecessary translatable strings.
  - Metadata widgets (Date, time, timedate).
  - Datatime widget: https://github.com/smalot/bootstrap-datetimepicker
  - Separate Event class instances with a parent namespace class: EventNamespace.
  - Add events for document signing app (uploaded detached signateure, signed document, deleted signature)
  - A configurable conversion process. Being able to invoke different binaries for file conversion, as opposed to the current libreoffice only solution.
  - A tool in the admin interface to mass (re)convert the files (basically the page count function, but then applied on all documents).
  - Find solution so that documents in watched folders are not processed until they are ready. Use case scanning directly to scanned folders.
