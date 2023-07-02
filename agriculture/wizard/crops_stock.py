from odoo import api, fields, models
from odoo.exceptions import UserError


class CropsStockWizard(models.TransientModel):
    _name = 'crops.stock.wizard'
    _description = 'Increment Stock'

    crops_id = fields.Many2one("crops.crops", string="CROPS", required=False, )
    product_id = fields.Many2one("product.product", string="", required=False, )

    quantity = fields.Float(string="",  required=False, )
    uom_id = fields.Many2one('uom.uom', 'Unit of Measure', required=True, )

    location_id = fields.Many2one("stock.location", string="Location", required=False, )
    location_dest_id = fields.Many2one("stock.location", string="DEST Location", required=False, )

    def create_stock_receipt(self):
        if self.quantity <= 0:
            raise UserError("You must add quantity")
        vals = {
            'picking_type_id': self.env.ref('stock.picking_type_in').id,
            'origin': f"CROPS {self.crops_id}",
            'move_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'product_uom_qty': self.quantity,
                'product_uom': self.uom_id.id,
                'crops_id': self.crops_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'name': f"CROPS {self.crops_id}",
            })]
        }
        stock_move = self.env['stock.picking'].create(vals)
        stock_move.action_confirm()

