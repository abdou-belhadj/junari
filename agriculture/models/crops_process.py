from odoo import api, fields, models, _


class CropsProcess(models.Model):
    _name = 'crops.process'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CROPS Process"

    crops_id = fields.Many2one("crops.crops", string="CROPS", required=False, )
    color = fields.Integer(related='crops_id.color')

    process_id = fields.Many2one("process.process", string="Process", required=True, )
    assigned_to = fields.Many2one("res.farmer", string="Farmer", required=False, )
    date_from = fields.Date('Date From', )
    date_to = fields.Date('Date To', )
    description = fields.Text(string="Description", required=False, )
    status = fields.Selection(
        string='Status',
        selection=[
            ('01_new', 'New'),
            ('02_in_progress', 'In Progress'),
            ('03_done', 'Done'),
            ('04_cancelled', 'Cancelled'),
        ],
        group_expand=lambda self, stages, domain, order: ['01_new', '02_in_progress', '03_done', '04_cancelled'],
        default='01_new',
        index=True)

    fleet_ids = fields.Many2many("fleet.vehicle", string="Tracktors/Fleets", default=False, )

    @api.onchange('process_id')
    def get_description(self):
        for rec in self:
            rec.description = rec.process_id.description.strip().replace('  ', '') if rec.process_id.description else ""
            rec.fleet_ids = rec.process_id.fleet_ids.ids
            rec.assigned_to = rec.process_id.assigned_to.id

    def done_process(self):
        for rec in self:
            rec.status = "03_done"

    def cancel_process(self):
        for rec in self:
            rec.status = "04_cancelled"

    def begin_process(self):
        for rec in self:
            rec.status = "02_in_progress"


class ProcessProcess(models.Model):
    _name = 'process.process'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=False, )
    description = fields.Text(string="Description", required=False, )
    fleet_ids = fields.Many2many("fleet.vehicle", string="Tracktors/Fleets", required=False, )
    assigned_to = fields.Many2one("res.farmer", string="Farmer", required=False, )
