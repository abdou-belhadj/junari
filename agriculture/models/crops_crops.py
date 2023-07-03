from odoo import api, fields, models, _


class CropsCrops(models.Model):
    _name = 'crops.crops'
    _description = 'Crops'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    @api.depends('crop_sequence', 'product_id.name')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.crop_sequence} - {rec.product_id.name}"

    name = fields.Char(string='Name', compute='_compute_name', store=True)

    active = fields.Boolean(string="Active", default=True, )

    crop_sequence = fields.Char('Name', copy=False, required=True, readonly=True, store=True,
                                default=lambda self: self.env['ir.sequence'].next_by_code('crops.crops'))

    product_id = fields.Many2one('product.product', 'Products', domain="[('crops_ok', '=', True)]",
                                 required=True, ondelete="cascade", delegate=True, )
    # image_1920 = fields.Image(related="product_id.image_1920", readonly=True, )

    color = fields.Integer('Color Index')

    date_from = fields.Date('Agriculture Date', )
    date_to = fields.Date('Harvest Date', )

    number_of_days = fields.Float(
        'Duration (Days)', compute='_compute_number_of_days', store=True, readonly=False, copy=False, tracking=True, )

    days_left_next_process = fields.Char(
        'Next_process_left', compute='_check_next_process', readonly=False, copy=False, store=True, )

    stage_id = fields.Many2one(
        'crops.stages',
        string='Stage', index=True, tracking=True, copy=False, ondelete='restrict', readonly=False, store=True,
        group_expand=lambda self, stages, domain, order: self.env['crops.stages'].search([], ),
        default=lambda self: self.env['crops.stages'].search([(['is_closing_opening', '=', True])],
                                                             order="sequence", limit=1).id,
    )
    is_harvest = fields.Boolean(related="stage_id.is_harvest", )
    process_ids = fields.One2many("crops.process", "crops_id", string="Process", required=False, )

    diseases_ids = fields.One2many("crops.disease", "crops_id", string="Disease", required=False, )

    process_count = fields.Integer(string="Processes Count", compute="_compute_processes_count", )
    picking_count = fields.Float(string="Picking Count", compute="_compute_picking_count", )
    uom_id = fields.Many2one(related='product_id.uom_id', required=True, )

    move_ids = fields.One2many('stock.move', 'crops_id', string="Stock Moves", copy=True)

    farmers = fields.Integer(string="Needed Farmer", required=False, )
    tracktors = fields.Integer(string="Needed Tracktors", required=False, )

    next_disease = fields.Date(string="Disease Check", compute="_check_next_disease", )

    @api.depends('process_ids')
    def _check_next_process(self):
        for rec in self:
            next_process = rec.process_ids.search(
                [('crops_id', '=', rec.id), ('status', '=', '01_new'), ('date_from', '!=', False)],
                order='date_from', limit=1)
            if next_process:
                delta = next_process.date_from - fields.Date.today()
                rec.days_left_next_process = f"{delta.days} days left for {next_process.process_id.name}"
            else:
                rec.days_left_next_process = f"No process date is mentionned."

    @api.depends('diseases_ids')
    def _check_next_disease(self):
        for rec in self:
            next_disease = rec.diseases_ids.search(
                [('crops_id', '=', rec.id), ('is_checked', '=', False), ('date', '>=', fields.Date.today())],
                order='date', limit=1)
            if next_disease:
                rec.next_disease = next_disease.date
            else:
                rec.next_disease = False

    @api.depends('process_ids')
    def _compute_processes_count(self):
        for rec in self:
            rec.process_count = len(rec.process_ids)

    @api.depends('move_ids')
    def _compute_picking_count(self):
        for rec in self:
            rec.picking_count = sum(self.move_ids.mapped('product_uom_qty'))

    @api.depends('date_from', 'date_to')
    def _compute_number_of_days(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                delta = rec.date_to - rec.date_from
                rec.number_of_days = delta.days
            else:
                rec.number_of_days = 0

    def action_view_crops_process(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "crops.process",
            "domain": [('crops_id', "=", self.id)],
            "context": {'default_crops_id': self.id},
            "name": _("CROPS"),
            'view_mode': 'kanban,tree,activity',
        }

    def action_view_stock_picking(self):
        return {
            "name": _(f"{self.name} Picking"),
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "domain": [('id', "in", self.move_ids.mapped('picking_id').ids)],
            'view_mode': 'tree,form,kanban',
            'context': {'create': False},
        }

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
