from odoo import http
from odoo.http import request
import json
import base64
import logging

_logger = logging.getLogger(__name__)

class RegistrationManagerController(http.Controller):

    @http.route(['/get_topics'], type='http', auth="public",website="False",cors="*", csrf=False)
    def get_topics(self):
        
        topics = request.env["registration_manager.topic"].sudo().search([])
        topic_list=[]
        for topic in topics:
            element = {
                'id': topic.id,
                'name': topic.name
            }
            topic_list.append(element)
        return json.dumps(topic_list)

    @http.route(['/add_registration'], type="http", auth="public", website="False", cors="*", csrf=False)
    def add_registration(self, **kw):
        vals_list = kw
        #handling the abstract file
        resume_file = vals_list.get("resume")

        if resume_file and not isinstance(resume_file, str):
            resume = base64.b64encode(resume_file.read())
            vals_list["filename"] = resume_file.filename
        else:
            resume = ""

        vals_list["state"] = "new"
        vals_list["resume"] = resume

        #handling the topic
        topic_id = vals_list.get("topic_id",None)
        topic_exist = request.env["registration_manager.topic"].sudo().search([('name', 'like', topic_id)])
        if topic_id and not topic_exist:
            topic = request.env["registration_manager.topic"].create({"name":topic_id})
            vals_list["topic_id"] = topic.id
        elif topic_id:
            vals_list["topic_id"] = topic_exist.id
        else:
            vals_list["topic_id"] = False

        #getting the authors
        authors = vals_list.get("authors", None)

        #removing the authors key so we can create the registration record directly
        #from the vals_list dict
        vals_list.pop("authors", None)
        record = request.env["registration_manager.registration"].create(vals_list)

        #Handling the authors
        if authors:
            authors_list = json.loads(authors)
            for author in authors_list:
                author["registration_id"] = record.id
                author_record = request.env["registration_manager.author"].create(author)

        #Sending email to user
        if vals_list.get('email'):
            record.sudo().action_send_email()

        print(vals_list.get('phone'))
        if vals_list.get('phone'):
           record.sudo().action_send_sms()

        json_res = {
            "msg": "registration sent!"
        }
        return json.dumps(json_res)

    @http.route(['/confirm_mail_registration/<string:token>/'], type="http", auth="public", website="False", cors="*", csrf=False)
    def confirm_mail_registration(self, token, **kw):
        record = request.env["registration_manager.registration"].search([("token", "=", token)])
        if (record):
            record.is_mail_confirmed = True
            return http.request.render(
                'registration_manager.mail_confirmation',
                {}
            )
