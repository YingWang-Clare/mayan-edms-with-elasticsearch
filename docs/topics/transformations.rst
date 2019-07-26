===============
Transformations
===============

Transformations are persistent manipulations to the previews of the stored 
documents. For example: a scanning equipment may only produce landscape PDFs. 
In this case a useful transformation for that document source would be to rotate 
all scanned documents by 270 degrees after being uploaded. By adding this 
transformation to the Mayan EDMS source that is connected to the scanner, all 
pages scanned via that source will inherit the transformation as they are 
created. The result is that whenever a document is uploaded from that scanner, 
it will appear in portrait orientation, instead of landscape orientation.

Transformations can also be added to existing documents by clicking on a
document's page and then clicking on "transformations". In this view the Actions 
menu will have a new option that reads "Create new transformation". Currently, 
the available transformations are: rotation, zoom, crop, and resize. Once the 
document image has been corrected, resubmit it for OCR for improved results.

Transformations are not destructive and do not physically modify the document 
file, they just modify the document's graphical representation.
