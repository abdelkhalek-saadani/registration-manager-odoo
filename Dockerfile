FROM odoo:15.0

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt