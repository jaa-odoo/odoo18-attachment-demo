🔍 Overview

This module enhances the standard invoice PDF in Odoo by dynamically linking each invoice line to its related attachment. It provides a clickable navigation system inside the generated invoice PDF, allowing users to jump directly to attachments embedded in the final PDF.

🎯 Key Features

- Attachment Field per Invoice Line: Adds a field (attachments_ids) to each invoice line to associate a document (e.g., product image, certificate, spec sheet).

- Clickable Attachment Numbers: The invoice PDF shows an attachment reference (e.g., "Attachment_5") next to each line, which users can click to jump to the actual attachment.

- PDF and Image Attachment Rendering:
    - PDF attachments are appended directly to the invoice PDF.
    - Non-PDF (image) attachments are rendered using a custom QWeb report.

- Automatic Internal Linking: Uses PyMuPDF to insert internal jump links in the PDF so the viewer can navigate easily.

- No Manual Editing Required: The entire process is automatic upon report generation—no user action is needed beyond selecting attachments.

🧩 Dependencies
Python Packages:

PyMuPDF (fitz) – for PDF link manipulation.
Make sure it's installed via pip:
    pip install PyMuPDF


Odoo Modules:

   account
   mail (required for attachment handling)


🛠️ Technical Details

 - Extends ir.actions.report to override _render_qweb_pdf_prepare_streams.

 - Modifies the invoice template (account.report_invoice_document) to display the attachment reference.

 - Includes a new QWeb report to render image attachments.

 - Adds an editable Many2many field attachments_ids in account.move.line for easy file selection.

 - Attachment field is enabled on the tree and form views for quick upload.


💡 Usage Tips

1. Go to Invoices and open or create a new invoice.

2. For each invoice line, use the Attachment field to upload or select an ir.attachment.

3. Print the invoice using the standard "Print Invoice" button.

4. Open the generated PDF. You'll see links like Attachment_3, which are clickable and jump to the embedded document pages.

