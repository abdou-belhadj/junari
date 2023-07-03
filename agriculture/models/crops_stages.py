from odoo import api, fields, models, _


class CropsStages(models.Model):
    _name = 'crops.stages'
    _description = "CROPS Stages"
    _rec_name = 'name'
    _order = "sequence, name"

    name = fields.Char(string="Name", required=False, )
    sequence = fields.Integer(string="Sequence", default=1, required=False, )
    description = fields.Html(string='Description')
    fold = fields.Boolean('Fold', )
    is_harvest = fields.Boolean('Is Harvest', )
    is_closing_opening = fields.Boolean(string="Closing / Opening", )
