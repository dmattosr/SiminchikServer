# -*- coding: utf-8 -*-
from flask import Flask
from flask import Flask, request, redirect, url_for
from flask_cors import CORS
from datetime import timedelta  
from flask import make_response, current_app  
from functools import update_wrapper
from flask import send_file, send_from_directory, safe_join, abort
import os
from hashlib import sha512
from werkzeug.utils import secure_filename
import json
from time import gmtime, strftime
import demjson
import utils
import generaldao as gdao
import appdao as adao
import webdao as wdao
import model

#UPLOAD_FOLDER = '/home/usuario/Escritorio/app_test/audio'
#UPLOAD_FOLDER = '/home/quechua/app_test/audio'
UPLOAD_FOLDER = '/home/ubuntu/app_final/app_test/audio'


app = Flask(__name__)
CORS(app)

app.config["CLIENT_AUDIOS_CHANCA"] = "/home/ubuntu/app_final/app_test/chanca/"
app.config["CLIENT_AUDIOS_COLLAO"] = "/home/ubuntu/app_final/app_test/collao/"

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):  
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route("/prompts_audios/<language>")
def get_image(language):
    print(language)
    if language == "chanca":
       return send_from_directory(app.config["CLIENT_AUDIOS_CHANCA"], filename=utils.getAudio(app.config["CLIENT_AUDIOS_CHANCA"]), as_attachment=True)
    if language == "collao":
       return send_from_directory(app.config["CLIENT_AUDIOS_COLLAO"], filename=utils.getAudio(app.config["CLIENT_AUDIOS_COLLAO"]), as_attachment=True)


@app.route('/upload', methods= ['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        file = request.files['files']
        print ("nombre audio: "+file.filename)

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and utils.allowed_file(file.filename):

            filename = secure_filename(file.filename)
            date = utils.createFile()
            url = UPLOAD_FOLDER+"/"+date

            if not os.path.exists(url):
                os.makedirs(url)

            app.config['UPLOAD_FOLDER'] = url
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            final = adao.selectAudio(filename,url)
        return final
    else:
        data = {'user_id': "0" ,'email': "0", 'audio_name':"0"}
        final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
        return final


@app.route('/dataupload', methods = ['POST'])
def post_upload():

    content = request.get_json()
    email = content['email']
    name = content['name']
    date = utils.createFile()
    url = UPLOAD_FOLDER+"/"+date
    upload_at = strftime("%d-%m-%Y", gmtime())
    final = adao.insertAudio(email,name,url,upload_at)
    return final


@app.route('/country', methods = ['POST'])
def country():

    data = gdao.selectCountry()
    return data


@app.route('/email', methods = ['POST'])
def selectAccount():

    content = request.get_json()
    email = content['email']
    data = gdao.selectUserEmail(email)
    return data


@app.route('/account_app', methods = ['POST'])
def account_app():

    content = request.get_json()
    email = content['email']
    password = sha512(content['password']).hexdigest()
    last_name = content['last_name']
    first_name = content['first_name']
    phone = content['phone']
    dni = content['dni']
    native_lang = content['native_lang']
    region_id = content['region_id']
    provincia_id = content['provincia_id']
    distrito_id = content['distrito_id']
    created_at = strftime("%d-%m-%Y", gmtime())
    data = gdao.insertUser_app(email,password,first_name,last_name,dni,phone,native_lang,region_id,provincia_id,distrito_id,created_at)
    a = '"email": "0"'
    if data.find(a) != -1:
	return data, 400
    else:
        return data

@app.route('/login_app', methods = ['POST'])
def logins_app():

    content = request.get_json()
    print(content)
    email = content['email']
    password = sha512(content['password']).hexdigest()
    login = gdao.login_app(email,password)
    print(login)
    a = '"email": "0"'
    if login.find(a) != -1:
	return login, 400
    else:
    	return login

@app.route('/email_app', methods = ['POST'])
def selectAccount_app():
    content = request.get_json()
    email = content['email']
    data = gdao.selectUserEmail_app(email)
    return data

@app.route('/count_text', methods = ['POST'])
def selectText():
    content = request.get_json()
    lang = content['lang']
    data = adao.select_text(lang)
    return data

@app.route('/upload_app', methods= ['GET', 'POST'])
def upload_file_app():

    if request.method == 'POST':

        file = request.files['files']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and utils.allowed_file(file.filename):

            filename = secure_filename(file.filename)
            filenames = filename.split('_')
            date = utils.createFile()
            url = UPLOAD_FOLDER+"/"+filenames[0]

            if not os.path.exists(url):
                os.makedirs(url)
            print 1
            app.config['UPLOAD_FOLDER'] = url
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print 2
            final = adao.record_audio(filename,date)
        return final
    else:
        data = {'user_app_id': "0" ,'dni': "0", 'audio_name':"0"}
        final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
        return final, status.HTTP_404_NOT_FOUND

@app.route('/lang', methods = ['POST'])
def language():

    data = gdao.selectLang()
    return data

@app.route('/vemail',methods = ['POST'])
def vemail():
    content = request.get_json()
    email = content['email']
    data = gdao.getEmail(email)
    return data

@app.route('/dni',methods = ['POST'])
def dni():
    content = request.get_json()
    dni = content['dni']
    data = gdao.getDNI(dni)
    return data

@app.route('/dialecto',methods = ['POST'])
def dialecto():
    content = request.get_json()
    ans_question = content['respuesta']
    data = gdao.getDialecto(ans_question)
    return data

@app.route('/dialecto_region',methods =['POST'])
def dialecto_region():
    content = request.get_json()
    print(content)
    dep = content['departamento']
    pro = content['provincia']
    dis = content['distrito']
    data = gdao.getDialectoRegion(dep,pro,dis)
    print(data)
    return data


if __name__ == '__main__':

    app.run(host = '0.0.0.0', debug = True)
