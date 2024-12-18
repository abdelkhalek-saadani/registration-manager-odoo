from odoo import models, fields, api
import hashlib
import time
from twilio.rest import Client
import os
import logging

_logger = logging.getLogger(__name__)


class registration(models.Model):
    _name = "registration_manager.registration"

    #registration form infos
    name = fields.Char(string="Nom")
    lastname = fields.Char(string="Prénom")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Tel")
    country = fields.Char(string="Pays")
    title = fields.Char(string="Titre")
    comment = fields.Char(string="Abstract")
    resume = fields.Binary(string="Abstract Fichier")
    registration= fields.Char(string="Registration")
    payement = fields.Char(string="Payement")
    institution = fields.Char(string="Institut")
    topic_id = fields.Many2one("registration_manager.topic",string="Les Sujets")
    type = fields.Char(string="Type")
    author_ids = fields.One2many("registration_manager.author",
                                 "registration_id",
                                 "Authors")

    #to display file name in form view
    filename = fields.Char(default="CV")

    #State done by admin
    state = fields.Selection(selection=[("new", "En attente"), ("accepted", "Acceptee"), ("rejected", "Refusee")],
                             default="new", string="Status")

    #used for email confirmation
    token = fields.Char(
        default=lambda self: self._compute_token(),
        readonly=True
    )
    is_mail_confirmed = fields.Boolean(default=False)

    #To limit normal users activity(reviewers)
    user_has_admin_group = fields.Boolean(string='User has Admin Group', compute='_compute_user_has_admin_group')

    reviewer_1_id = fields.Many2one("res.users", "Reviewer 1")
    reviewer_2_id = fields.Many2one("res.users", "Reviewer 2")

    notice_1 = fields.Selection(selection=[("yes", "Oui"), ("no", "Non")], string="Avis 1")
    notice_2 = fields.Selection(selection=[("yes", "Oui"), ("no", "Non")], string="Avis 2")
    comment_1 = fields.Text("Commentaire du Reviewer 1")
    comment_2 = fields.Text("Commentaire du Reviewer 2")

    user_is_reviewer_1 = fields.Boolean(compute='_compute_user_is_reviewer_1')
    user_is_reviewer_2 = fields.Boolean(compute='_compute_user_is_reviewer_2')

    def _compute_user_is_reviewer_1(self):
        current_user_id = self.env.user.id
        for record in self:
            reviewer_id = record.reviewer_1_id.id
            record.user_is_reviewer_1 = (reviewer_id == current_user_id)

    def _compute_user_is_reviewer_2(self):
        current_user_id = self.env.user.id
        for record in self:
            reviewer_id = record.reviewer_2_id.id
            record.user_is_reviewer_2 = (reviewer_id == current_user_id)

    def _compute_user_has_admin_group(self):
        for record in self:
            record.user_has_admin_group = self.env.user.has_group('base.group_erp_manager')
    def _compute_token(self):
        secret = "secret_conf"
        current_time = str(time.time())
        combined_string = secret + current_time
        hash_object = hashlib.sha256()
        hash_object.update(combined_string.encode("utf-8"))
        token = hash_object.hexdigest()
        return token

    def action_send_sms(self):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
        _logger.warning("account_sid,|, auth_token,|, twilio_number")
        _logger.warning(account_sid,"|", auth_token,"|", twilio_number)
        if account_sid and auth_token and twilio_number:
            for rec in self:
                phone_number = rec.phone
                phone_number = phone_number.replace(" ","")
                if (phone_number[:4] != "+216"):
                    phone_number = "+216" + phone_number
                if rec.lastname:
                    lastname = rec.lastname
                else:
                    lastname = ""
                if rec.name:
                    name = rec.name
                else:
                    name = ""
                message_content = "Hello " + name + " " + lastname + ", your registration is sent successfully, we sent you an email for Confirmation"
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_= twilio_number,
                to=phone_number,
                body=message_content
            )
            _logger.info("Message sent successfully")
            
        else:
            _logger.info("messagae not sent, missing env variables")


    def action_send_email(self):
        mail_template = self.env.ref('registration_manager.registration_email_template')
        mail_template.send_mail(self.id, force_send=True)


    def accept(self):
        for rec in self:
            rec.state = "accepted"
        return True

    def reject(self):
        for rec in self:
            rec.state = "rejected"
        return True
