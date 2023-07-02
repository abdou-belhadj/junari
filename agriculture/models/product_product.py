from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    crops_ok = fields.Boolean('Is Crops', default=False)
