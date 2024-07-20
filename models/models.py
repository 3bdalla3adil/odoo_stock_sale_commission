# -*- coding: utf-8 -*-
from odoo import models, fields, api

  #===========================================================================================================
  #===  PIPELINE  =========== PURCHASE ==> STOCK ==> SALES ==> ACCOUNT =======================================
  #===========================================================================================================

  #ToDo:Identify Commissioner (Contact)
  #ToDo:Identify Commissioned Product (Stock)
  #ToDo:Identify Commission percentage value (Stock)
  #ToDo:Mark Commissioned PO as Commissioned Order (purchase)
  #ToDo:Mark PO Commissioned Order Product as consignment product (purchase)
  #ToDo:Identify Expense Account, Income Account, And Prepayment Account (sales,account)


class RP(models.Model):
    _inherit = 'res.partner'

    is_commissioner = fields.Boolean(string="Is a Commissioner")


class PO(models.Model):
    _inherit = 'purchase.order'

    commissioned_order = fields.Boolean(string="Commissioned Order")
    consignment_product = fields.Boolean(string="Consignment Product")
    #ToDo:Create Percentage Float Field

    def button_confirm(self):
        res = super(PO).button_confirm()


class SP(models.Model):
    _inherit = 'stock.picking'

    commission_percentage = fields.Float(string="Commission Percentage")


class SO(models.Model):
    _inherit = 'sale.order'

    commissioned_order = fields.Boolean(string="Commissioned Order")
    commissioner_id = fields.Many2one('res.partner', string="Commissioner")
    # value = fields.Float()

    def action_confirm(self):
        res = super(SO, self).action_confirm()
        if self.invoice_status == 'to invoice':
            self.create_invoice()
        return res

    def create_invoice(self):
        invoice_vals = {
            'partner_id': self.partner_id.id,
            'type': 'out_invoice',
            'invoice_line_ids': [(0, 0, {
                'name': line.product_id.name,
                'quantity': line.product_uom_qty,
                'price_unit': line.price_unit,
                'account_id': self.determine_invoice_account(line.product_id),
            }) for line in self.order_line],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        invoice.action_post()

    def determine_invoice_account(self, product):
        # determine account based on product or settings
        settings = self.env['res.config.settings'].search([])  # Assuming ID 1 for settings
        if product.type == 'service':
            return settings.income_account_id.id
        elif product.type == 'product':
            return settings.inventory_account_id.id
        else:
            return settings.default_account_id.id

    # is_rebate_customer = fields.Boolean('Is Rebate Customer')
    # follow_parent_company_rebate = fields.Boolean('Follow Parent Company Rebate', default=True)
    # rebate_percentage_ids = fields.One2many('rebate.percentage', 'partner_id', string='Rebate Percentage')
    # auto_reconcile = fields.Boolean('Auto Reconcile')


class AJ(models.Model):
    _inherit = "account.journal"

    commission_journal = fields.Boolean('Commission Journal')


# class RCS(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     expense_account_id = fields.Many2one('account.account', string="Expense Account")
#     income_account_id = fields.Many2one('account.account', string="Income Account")
#     prepayment_account_id = fields.Many2one('account.account', string="Prepayment Account")