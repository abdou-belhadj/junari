from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    crops_id = fields.Many2one("crops.crops", string="CROPS", required=False, )
