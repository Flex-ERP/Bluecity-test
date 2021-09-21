# -*- coding: utf-8 -*-


from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    second_hand_tax = fields.Boolean(string="Second Hand Tax", copy=False)
    fiscal_tax_ids = fields.Many2many(
        'account.tax', string="Fiscal Taxes", copy=False)

    @api.onchange('second_hand_tax')
    def update_fiscal_position(self):
        for rec in self:
            rec.fiscal_position_id = False
            rec.order_line = False
            rec.fiscal_tax_ids = False

    @api.onchange('fiscal_position_id')
    def onchange_fiscal_position(self):
        for record in self:
            fiscal_tax = []
            if record.fiscal_position_id and record.second_hand_tax:
                if record.fiscal_position_id.tax_ids:
                    for taxes in record.fiscal_position_id.tax_ids:
                        fiscal_tax.append(taxes.tax_src_id.id)
                    record.fiscal_tax_ids = fiscal_tax
            else:
                taxes_ids = self.env['account.tax'].search(
                    [('type_tax_use', '=', 'purchase'), ('company_id', '=', record.company_id.id)])
                for tax in taxes_ids:
                    fiscal_tax.append(tax.id)
                record.fiscal_tax_ids = fiscal_tax
