# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	lot_id = fields.Many2one('stock.production.lot', string="Lot/Serial", copy=False)
	tax_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), 
		('active', '=', True)], compute="get_lot_taxes")

	@api.depends('lot_id')
	def get_lot_taxes(self):
		for rec in self:
			if rec.lot_id and rec.lot_id.tax_ids:
				rec.tax_id = [(6, 0, rec.lot_id.tax_ids.ids)]
			else:
				rec.tax_id = False


	def _prepare_procurement_values(self, group_id=False):
	    res = super()._prepare_procurement_values(group_id)
	    if self.product_id.type == 'product':
	    	res.update({'lot_id': self.lot_id.id})
	    return res