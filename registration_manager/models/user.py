from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    country = fields.Char("Pays")
    institution = fields.Char("Institut")
    phone_number = fields.Char("Tel")
    topic_id = fields.Many2one("registration_manager.topic", "Topic")

    @api.model
    def create(self, vals_list):
        vals_list["in_group_13"] = True     # To Set new Created users as Reviewers by default
        return super(ResUsers, self).create(vals_list)
