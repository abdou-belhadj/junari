from odoo import api, fields, models, _


class CropsDisease(models.Model):
    _name = 'crops.disease'
    _description = "CROPS Disease"

    crops_id = fields.Many2one("crops.crops", string="CROPS", required=False, )
    disease_id = fields.Many2one("disease.disease", string="Disease", required=True, )
    date_from = fields.Date('Date From', )
    date_to = fields.Date('Date To', )
    description = fields.Char(string="Description", required=False, )
    is_done = fields.Boolean(string="Done", )

    @api.onchange('disease_id')
    def get_description(self):
        for rec in self:
            rec.description = rec.disease_id.description

class DiseaseDisease(models.Model):
    _name = 'disease.disease'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=False, )
    description = fields.Char(string="Description", required=False, )
