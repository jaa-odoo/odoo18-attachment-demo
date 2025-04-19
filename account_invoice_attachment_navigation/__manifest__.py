# -*- encoding: utf-8 -*-

{
    "name": "Invoice Attachments Navigation",
    "version": "18.0.1.0.0",
    "summary": "Adds dynamic attachment links to invoice sections with navigation support.",
    "description": """
        This module enhances the standard invoice functionality in Odoo by:
        - Adding a dynamic attachment number for each invoice line section.
        - Generating attachment links for each attachment number.
        - Enabling users to click the attachment number to navigate directly to the corresponding attachment.
        The actual content of the attachment is not relevant—this module only implements the navigation logic.
    """,
    "category": "Utility Tools",
    "author": "Puro.earth Oy",
    "maintainer": "Puro.earth Oy",
    "website": "https://puro.earth/",
    "license": "LGPL-3",

    "depends": [
        "account",  # Depends on the Accounting module for invoices
        "mail"  # Required for attachment functionality (ir.attachment)
    ],

    "external_dependencies": {
        "python": [
            "pymupdf",  # PyMuPDF
            "frontend"
        ]
    },

    "data": [
        "views/account_move_view.xml",  # Invoice form and tree view extension for attachment links
        "report/invoice_report_template.xml"  # QWeb template for invoice report with clickable attachment links
    ],

    "installable": True,  # Can be installed
    "application": False,  # Not an application, just a module
    "auto_install": False  # Does not auto-install other dependencies
}
