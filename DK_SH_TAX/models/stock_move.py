# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    tax_code = fields.Many2many(
        related='purchase_line_id.taxes_id', string="Tax Code", copy=False)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    tax_code = fields.Many2many(
        related='move_id.tax_code', string="Tax Code", copy=False)
