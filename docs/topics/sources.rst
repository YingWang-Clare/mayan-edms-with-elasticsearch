=======
Sources
=======

Document sources define places from which documents can be uploaded or gathered.

The current document sources supported are:

- Web - ``HTML`` forms with a ``Browse`` button that will open the file dialog
  when clicked to allow selection of files in the user's computer to be
  uploaded as documents.
- POP3 email - Provide the email, server and credential of a ``POP3`` based
  email to be scanned periodically for email. The body of the email is uploaded
  as a document and the attachments of the email are uploaded as separate
  documents.
- IMAP email - Same as the ``POP3`` email source but for email accounts using
  the ``IMAP`` protocol.
- Watch folder - A filesystem folder that is scanned periodically for files.
  Any file in the watch folder is automatically uploaded.
- Staging folder - Folder where networked attached scanned can save image
  files. The files in these staging folders are scanned and a preview is
  generated to help the process of upload. Staging folders and Watch folders
  work in a similar way with the main difference being that Staging folders are
  interactive while Watch folders are automatic; documents in a Watch folder
  are uploaded periodically and documents in a Staging folder remain indefinitely
  there until an user uploads them. A preview for files in a Staging folder is
  also provided. An example of Staging folder use is when multiple people
  are scanning documents but only one person must be allowed to upload those
  documents. This one person examines the scans quality and decides what to
  upload and what to reject and have re-scanned. Watch folders can be used
  when the quality of the scans is irrelevant or when they will be known
  to be of good quality, such as when receiving e-faxes as PDFs.

Document source can be configure to allow document bundles to uploaded as
compressed files which are decompressed and their content uploaded as separate
documents. This feature is useful when migrating from another document
manager system.
