# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    x_attachment_id = fields.Many2one(
        comodel_name='ir.attachment',
        string='Attachment',
        readonly=False,
        help="Attach a file to this invoice line for reference or documentation."
    )
    attachments_ids = fields.Many2many(
        comodel_name='ir.attachment',
        string="Attachments",
    )
