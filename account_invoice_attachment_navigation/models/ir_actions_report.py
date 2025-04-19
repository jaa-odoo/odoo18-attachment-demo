import io
import fitz  # PyMuPDF
from odoo import models
from odoo.tools import pdf
from odoo.tools.pdf import OdooPdfFileReader, OdooPdfFileWriter
import logging

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
        res = super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids)
        if not res_ids:
            return res

        report = self._get_report(report_ref)
        if report.report_name != 'account.report_invoice':
            return res

        account_moves = self.env['account.move'].browse(res_ids)
        global_counter = 0  # Global attachment counter across all moves

        for move in account_moves:
            stream_list = []
            main_stream = res[move.id]['stream']
            stream_list.append(main_stream)

            # Collect all attachments from invoice lines
            attachments = move.invoice_line_ids.mapped('attachments_ids').filtered(lambda a: a)

            move_reader = OdooPdfFileReader(main_stream, strict=False)
            output_pdf = OdooPdfFileWriter()
            output_pdf.appendPagesFromReader(move_reader)

            page_counter = len(move_reader.pages)
            attachment_metadata = []  # Store (keyword, start_page)

            for attachment in attachments:
                try:
                    global_counter += 1
                    keyword = f"Attachment_{global_counter}"

                    if attachment.mimetype == 'application/pdf':
                        attachment_stream = pdf.to_pdf_stream(attachment)
                    else:
                        data['attachment'] = attachment
                        alt_render = self._render_qweb_pdf_prepare_streams(
                            'account_invoice_attachment_navigation.report_invoice_document_dynamic_sheet_img',
                            data,
                            res_ids=[move.id]
                        )
                        attachment_stream = alt_render[move.id]['stream']

                    reader = OdooPdfFileReader(attachment_stream, strict=False)
                    attachment_metadata.append((keyword, page_counter))
                    page_counter += len(reader.pages)

                    output_pdf.appendPagesFromReader(reader)
                    stream_list.append(attachment_stream)
                except Exception as e:
                    _logger.warning(f"Attachment {attachment.id} could not be added to invoice {move.name}: {e}")

            # Finalize merged PDF
            new_pdf_stream = io.BytesIO()
            output_pdf.write(new_pdf_stream)
            new_pdf_stream.seek(0)

            final_doc = fitz.open(stream=new_pdf_stream.getvalue(), filetype='pdf')

            # Insert jump links for all valid keywords
            for keyword, target_page in attachment_metadata:
                link_created = False

                for page_num in range(len(final_doc)):
                    if page_num >= attachment_metadata[0][1]:
                        break  # Skip attachment pages

                    page = final_doc[page_num]
                    found_rects = page.search_for(keyword)
                    for rect in found_rects:
                        page.insert_link({
                            "kind": fitz.LINK_GOTO,
                            "from": rect,
                            "page": target_page,
                        })
                        link_created = True

                if not link_created:
                    _logger.warning(f"No label found for {keyword} in invoice {move.name}")

            res[move.id]['stream'] = io.BytesIO(final_doc.write())
            final_doc.close()

            # Clean up all streams
            for s in stream_list:
                try:
                    s.close()
                except Exception:
                    pass

        return res
