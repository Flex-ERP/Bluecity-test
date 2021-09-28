# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    tax_ids = fields.Many2many('account.tax', string="Taxes", copy=False)

    def get_lot_taxes(self, lot):
        lot_id = self.search([('name','=', lot[0])])
        tax_name = []
        if lot_id:
            for tax in lot_id.tax_ids:
                tax_name.append({'id':tax.id,'name':tax.name})
        return tax_name


class StockRule(models.Model):
  _inherit = "stock.rule"

  def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        res = super()._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        res['lot_id'] = values.get('lot_id', False)
        return res


class StockMove(models.Model):
    _inherit = "stock.move"

    lot_id = fields.Many2one('stock.production.lot', string="LOT")

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        res = super()._prepare_move_line_vals(quantity, reserved_quant)
        if self.lot_ids:
            res.update({
                'lot_id': self.lot_ids.ids[0]
                })
        return res

    @api.depends('move_line_ids', 'move_line_ids.lot_id', 'move_line_ids.qty_done')
    def _compute_lot_ids(self):
        domain_nosuggest = [('move_id', 'in', self.ids), ('lot_id', '!=', False), '|', ('qty_done', '!=', 0.0), ('product_qty', '=', 0.0)]
        domain_suggest = [('move_id', 'in', self.ids), ('lot_id', '!=', False), ('qty_done', '!=', 0.0)]
        lots_by_move_id_list = []
        for domain in [domain_nosuggest, domain_suggest]:
            lots_by_move_id = self.env['stock.move.line'].read_group(
                domain,
                ['move_id', 'lot_ids:array_agg(lot_id)'], ['move_id'], 
            )
            lots_by_move_id_list.append({by_move['move_id'][0]: by_move['lot_ids'] for by_move in lots_by_move_id})
        for move in self:
            move.lot_ids = [(6, 0, move.lot_id.ids)]