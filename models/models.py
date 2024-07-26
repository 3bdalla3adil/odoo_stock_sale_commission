# -*- coding: utf-8 -*-
from odoo import models, fields, api

  #===========================================================================================================
  #==== PIPELINE ============ PURCHASE ==> STOCK ==> SALES ==> ACCOUNT =======================================
  #===========================================================================================================

  #ToDo:Identify Expense Account, Income Account, And Prepayment Account (sales,account) need to configure properity accounts first


class RP(models.Model):
    _inherit = 'res.partner'

    is_commissioner = fields.Boolean(string="Is a Commissioner")


class PO(models.Model):
    _inherit = 'purchase.order'

    is_commissioned = fields.Boolean(string="Commissioned Order")
    commissioner_id = fields.Many2one('res.partner',domain=[('is_commissioner','=',True)], string="Commissioner")

    
    def button_confirm(self):
        res = super(PO,self).button_confirm()
        if self.commissioner_id:
            self.is_commissioned = True
            self.product_id.is_consignment = True

        return res


class PT(models.Model):
    _inherit = 'product.template'
    """Class inherited to add the custom fields to the model"""

    commission_percentage = fields.Float(string="Commission %")
    is_consignment = fields.Boolean(string="Is Consignment")
    commissioner_id = fields.Many2one('res.partner',domain=[('is_consignment','=',True)], string="Commissioner")


class PP(models.Model):
    _inherit = 'product.product'
    """Class inherited to add the custom fields to the model"""

    commission_percentage = fields.Float(string="Commission %")
    is_consignment = fields.Boolean(string="Is Consignment")
    commissioner_id = fields.Many2one('res.partner',domain=[('is_consignment','=',True)], string="Commissioner")


class SP(models.Model):
    _inherit = 'stock.picking'

    is_commission = fields.Boolean(string="Is Commissioned", compute="_compute_is_commission")

    @api.depends('product_id')
    def _compute_is_commission(self):
        if self.product_id.is_consignment:
            self.is_commission = True
    
class AM(models.Model):
    _inherit = 'account.move'   

    def action_confirm(self):
        
        res = super(AM,self).action_confirm()

        for line in self.invoice_line_ids:
            if line.product_id.is_consignment:
                line.unit_price /= self.product_id.commission_percentage
                
        return res

class SO(models.Model):
    _inherit = 'sale.order'

    commissioner_id = fields.Many2one('res.partner',domain=[('is_commissioner','=',True)], string="Commissioner")


    def action_confirm(self):
        
        res = super(SO,self).button_confirm()

        for line in self.order_line:
            if line.product_id.is_consignment:
                line.unit_price /= self.product_id.commission_percentage
        return res

