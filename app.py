# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_admin import Admin
import json
from flask_recaptcha import ReCaptcha
import requests
import time
import grequests
from models import db
from models import BaseTerm
import logging

app = Flask(__name__)

POSTGRES = {
    'user': 'flask',
    'pw': 'flask',
    'db': 'flask',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = False
app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_SITE_KEY'] = '6LeRyIAUAAAAAIoeWckcPcA9yihVGsZOzY6aqUdW'
app.config['RECAPTCHA_SECRET_KEY'] = '6LeRyIAUAAAAAHZ823WB9sRY0KXMu5T_UxMiwaGS'
recaptcha = ReCaptcha(app=app)
app.config['JSON_AS_ASCII'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)
## flask admin
admin = Admin(app, name='Unbabel Translator', template_mode='bootstrap3')

def api_credentials():
    username = "fernando.gomes"
    apikey = "c857ef43875e7c2e61934de6b2f57accfc3bddcf"
    return username, apikey


def translate_uid(uids):
    """

    :param uids: comma separated uid
    :return: a dict with uid as key and [status, translated value] as value
    """
    url = "https://sandbox.unbabel.com/tapi/v2/translation/"
    username, apikey = api_credentials()
    headers = {
        'Authorization': 'ApiKey %s:%s' % (username, apikey),
        'Content-Type': 'application/json',
    }
    result = {}
    if uids:
        for uid in uids.split(','):

            record = BaseTerm.query.filter_by(uid=uid).first()
            if record:
                if record.status != 'completed':
                    attempt = 1
                    status = 'new'
                    # while status != 'completed':
                    logging.info("attempt ........: %s", attempt)
                    r = requests.get('%s%s/' % (url, uid), headers=headers)
                    status = r.json().get('status')
                    record.status = status
                    db.session.commit()
                    attempt += 1

                    if status == 'completed':
                        record.translated_term = r.json().get('translatedText')
                    db.session.commit()
                result[uid] = [record.status, record.translated_term]
    logging.info("result : %s",result)
    return result




@app.route('/checkStatus')
def background_check_status():
    terms_to_translate = request.args.get('terms_to_translate')
    result = translate_uid(terms_to_translate)
    return json.dumps(result)


@app.route('/queueTerm')
def queue_term():
    # Note : we do not need to verify recaptcha in python
    #        it is validated in .js ( there is a limitation to validate in python because
    #        we are not calling method queue_term by form's post attribute
    """
    input_term : text requested to be tranlsated
    unique_hash : a unique string generated for input_term to identify the columns
    :return:
    """
    ## check if term exists in database
    logging.info("Request args : %s " %request.args)
    input_term = request.args.get('input', '').strip().encode('utf-8')
    unique_hash = request.args.get('unique_hash', '')
    # insert term in database if not exists
    record = BaseTerm.query.filter_by(term=input_term).first()
    uid = False
    logging.info("Translating term : %s" %input_term)
    if not record:
        record = BaseTerm(term=input_term, uid=uid)
        db.session.add(record)
        db.session.commit()
    # don't make request for error== 400, invalid JSON
    if not record.uid and record.status != 'error':
        username , apikey = api_credentials()
        headers = {
            'Authorization': 'ApiKey %s:%s' % (username, apikey),
            'Content-Type': 'application/json',
        }
        url = "https://sandbox.unbabel.com/tapi/v2/translation/"
        text = input_term  # "Hello world" # input_term TODO: check some terms won't respond correctly probably like numbers
        source_language = "en"
        target_language = "es"
        text_format = "text"

        data = '{"text" : "%s", "source_language" : "%s", "target_language" : "%s", "text_format" : "%s"}' % (
            text, source_language, target_language, text_format)
        logging.info("Queueing term  :   %s " %input_term)
        r = requests.post(url, headers=headers, data=data)
        if r.status_code == 201:
            uid = r.json().get('uid')
        else:
            if r.status_code == 400:
                if r.json().get('error'):
                    record.status = 'error'
                    record.translated_term = r.json().get('error')
                    db.session.commit()

            logging.critical("Request Failed with response code : %s" %r.status_code)
        if uid and record:
            record.uid= uid
            db.session.commit()
    return json.dumps({unique_hash:record.uid})



@app.route("/")
def main():
    """ Render Homepage """
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run()
