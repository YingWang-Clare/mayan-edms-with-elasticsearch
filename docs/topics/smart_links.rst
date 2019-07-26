===========
Smart links
===========

Smart links are a way to link documents without changing how they are organized
in their respective indexes. Smart links are useful when two documents are
related somehow but are of different type or different hierarchical units.

Example: A patient record can be related to a prescription drug information
document, but they each belong to their own :doc:`indexes`.

Smart links are rule based, but don't create any organizational structure.
Smart links just show the documents that match the rules as evaluated against
the metadata or properties of the currently displayed document.

Indexes are automatic hierarchical units used to group documents, smart links
are automatic references between documents.

Example:

- Document type: ``Patient records``
- Metadata type: ``Prescription``, associated as an optional metadata for the document type ``Patient records``.

- Document type: ``Prescription information sheets``

A smart link with the following condition, will automatically links patient
records to the prescription information sheets based on the value of the
metadata type of the patient record.

.. code-block:: bash

    foreign label is equal to {{ document.metadata_value_of.prescription }}
