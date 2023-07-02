from odoo import api, fields, models, _


class CropsCrops(models.Model):
    _name = 'crops.crops'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'product_id'

    active = fields.Boolean(string="Active", default=True, )

    product_id = fields.Many2one('product.product', 'Products', domain="[('crops_ok', '=', True)]",
                                 required=True, ondelete="cascade", )
    color = fields.Integer('Color Index')
    image_1920 = fields.Image(related="product_id.image_1920", readonly=True, )

    date_from = fields.Date('Agriculture Date', )
    date_to = fields.Date('Harvest Date', )

    number_of_days = fields.Float(
        'Duration (Days)', compute='_compute_number_of_days', store=True, readonly=False, copy=False, tracking=True, )

    stage_id = fields.Many2one(
        'crops.stages',
        string='Stage', index=True, tracking=True, copy=False, ondelete='restrict', readonly=False, store=True,
        group_expand=lambda self, stages, domain, order: self.env['crops.stages'].search([], ),
        default=lambda self: self.env['crops.stages'].search([], order="sequence", limit=1).id,
    )

    process_ids = fields.One2many("crops.process", "crops_id", string="Process", required=False, )

    diseases_ids = fields.One2many("crops.disease", "crops_id", string="Disease", required=False, )

    process_count = fields.Integer(string="Processes Count", compute="_compute_processes_count", )

    move_ids = fields.One2many('stock.move', 'crops_id', string="Stock Moves", copy=True)

    @api.depends('process_ids')
    def _compute_processes_count(self):
        for rec in self:
            rec.process_count = len(rec.process_ids)

    def action_view_crops_process(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "crops.process",
            "domain": [('crops_id', "=", self.id)],
            "context": {'default_crops_id': self.id},
            "name": _("CROPS"),
            'view_mode': 'kanban,activity',
        }

    @api.depends('date_from', 'date_to')
    def _compute_number_of_days(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                delta = rec.date_to - rec.date_from
                rec.number_of_days = delta.days
            else:
                rec.number_of_days = 0

    def create_stock_receipt(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "crops.stock.wizard",
            "context": {'default_crops_id': self.id,
                        'default_product_id': self.product_id.id,
                        'default_uom_id': self.product_id.uom_id.id,
                        'default_location_id': self.env.ref('agriculture.crops_location').id,
                        'default_location_dest_id': self.env.ref('stock.stock_location_stock').id,
                        },
            "name": _("CROPS STOCK"),
            'view_mode': 'form',
            'target': 'new',
        }


class CropsStages(models.Model):
    _name = 'crops.stages'
    _description = "CROPS Stages"
    _rec_name = 'name'
    _order = "sequence, name"

    name = fields.Char(string="Name", required=False, )
    sequence = fields.Char(string="Sequence", default=1, required=False, )
    description = fields.Html(string='Description')
    fold = fields.Boolean('Fold', )
