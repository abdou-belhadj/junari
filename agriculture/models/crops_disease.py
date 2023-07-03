from odoo import api, fields, models, _


class CropsDisease(models.Model):
    _name = 'crops.disease'
    _description = "CROPS Disease"

    crops_id = fields.Many2one("crops.crops", string="CROPS", required=False, )
    disease_id = fields.Many2one("disease.disease", string="Disease", required=True, )
    date = fields.Date('Check Date', )
    description = fields.Text(string="Description", required=False, )
    is_checked = fields.Boolean(string="Checked", )

    def disease_checked(self):
        for rec in self:
            rec.is_checked = True

    @api.onchange('disease_id')
    def get_description(self):
        for rec in self:
            rec.description = rec.disease_id.description.strip().replace('  ', '') if rec.disease_id.description else ""


class DiseaseDisease(models.Model):
    _name = 'disease.disease'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=False, )
    description = fields.Text(string="Description", required=False, )
