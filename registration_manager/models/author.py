from odoo import models, fields


class registration(models.Model):
    _name = "registration_manager.author"

    #Author form infos
    name = fields.Char(string="Nom")
    lastname = fields.Char(string="Prénom")
    email = fields.Char(string="Email")
    affiliation = fields.Char(string="Affiliation")
    registration_id = fields.Many2one("registration_manager.registration",
                                    "registration")