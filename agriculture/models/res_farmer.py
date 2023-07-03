from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_farmer = fields.Boolean('Is Farmer', default=False)


class ResFarmer(models.Model):
    _name = 'res.farmer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=False, ondelete="cascade")

    first_name = fields.Char('First Name', translate=True)
    middle_name = fields.Char('Middle Name', size=128)
    last_name = fields.Char('Last Name', size=128, required=True)

    birth_date = fields.Date('Birth Date', required=True)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], 'Gender', required=True)
    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Blood Group')

    nationality = fields.Many2one('res.country', 'Nationality')
    nationality_code = fields.Char(related='nationality.code')

    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')

    @api.model
    def create(self, values):
        values['is_farmer'] = True
        return super(ResFarmer, self).create(values)

    @api.model
    def default_get(self, fields):
        res = super(ResFarmer, self).default_get(fields)
        if 'nationality' in fields and not res.get('nationality'):
            res['nationality'] = self.env.ref('base.uk')
        return res

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        if not self.middle_name:
            self.name = str(self.first_name) + " " + str(
                self.last_name)
        else:
            self.name = str(self.first_name) + " " + str(
                self.middle_name) + " " + str(self.last_name)

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))
