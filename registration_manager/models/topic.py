from odoo import models, fields



class Topic(models.Model):
    _name = "registration_manager.topic"

    
    name = fields.Char(string="Topic")
    description = fields.Text(string="Description")
    