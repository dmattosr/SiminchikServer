# -*- coding: utf-8 -*-
import sys
import re, string
import urllib2
import demjson
import json
import connectiondb as conn
import utils
import message_service as mservice
from validate_email import validate_email
import requests
import pandas as pd

reload(sys)
sys.setdefaultencoding('Cp1252')

def selectUserID(email):

    query = "SELECT user_id FROM user WHERE email = '%s' LIMIT 1;" %(email)
    data = ""
    cursor = conn.run_query(query,data)
    user_id = ""

    for user in cursor:
        user_id = user
    
    return user_id


def insertUser(email,password,last_name,first_name,phone,country_id,created_at):

    em = selectUserID(email)
    if (em == ''):
        query = "INSERT INTO user (first_name, last_name, phone, country_id, email, password, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s) ;"
        data = (first_name, last_name, phone, country_id, email, password, created_at)
        conn.run_query(query,data)
        user_id = selectUserID(email)
        data = {'user_id': user_id ,'email': email, 'first_name':first_name, 'last_name': last_name}
        final = json.dumps(data,ensure_ascii=False).encode('utf8')
        return final
    else:
        data = {'user_id': '0' ,'email': '0', 'first_name':'0', 'last_name': '0'}
        final = json.dumps(data,ensure_ascii=False).encode('utf8')
        return final


def selectUserEmail(email):

    em = selectUserID(email)

    if (em == ''):

        data = {'user_id': '0' ,'email': '0', 'first_name':'0', 'last_name': '0'}
        final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
        return final

    else:

        query = "SELECT user_id, first_name, last_name FROM user WHERE user_id = %s LIMIT 1;"
        data = (em)
        cursor = conn.run_query(query,data)
        c = 0
        user_id = ""
        first_name = ""
        last_name = ""

        for (user, fname,lname) in cursor:

            user_id = user
            first_name = fname
            last_name = lname

        data = {'user_id': user_id ,'email': email, 'first_name':first_name, 'last_name': last_name}
        final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
        return final


def login(email,password):

        query = "SELECT password,user_id, first_name, last_name FROM user WHERE email = '%s' LIMIT 1; " %(email)
        data = ""
        cursor = conn.run_query(query,data)

        c = 0
        user_id = ""
        first_name = ""
        last_name = ""

        for (password_bd, user, fname,lname) in cursor:
                password_bd = str(password_bd)
                password_bd = re.sub('[%s]' % re.escape(string.punctuation),"", password_bd).lower()
                if password == password_bd:
                        c = 1
                        user_id = user
                        first_name = fname
                        last_name = lname

        if c == 1:

                data = {'user_id': user_id ,'email': email, 'first_name':first_name, 'last_name': last_name}
                final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
                return final
        else:

                data = {'user_id': '0' ,'email': '0', 'first_name':'0', 'last_name': '0'}
                final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
                return final


def selectCountry():

    query = "SELECT country_id, name FROM country;"
    data = ""
    cursor = conn.run_query(query,data)

    country_id = []
    name = []

    for (ids, c) in cursor:

        country_id.append(ids)
        name.append(c)

    i = 0

    country = []

    for a in country_id:
        
        p = {'country_id':country_id[i],'name':name[i]}
        country.append(p)
        i = i + 1

    data = {'countries': country}
    final = json.dumps(data,ensure_ascii=False).encode('utf8')
    return final

def selectLang():

    query = "SELECT language_id, iso, name FROM language;"
    data = ""
    cursor = conn.run_query(query,data)

    language_id = []
    iso = []
    name = []

    for (ids, i, names) in cursor:

        language_id.append(ids)
        iso.append(i)
        name.append(names)

    i = 0

    language = []

    for a in language_id:
        
        p = {'language_id':language_id[i],'iso': iso[i],'name':name[i]}
        language.append(p)
        i = i + 1

    data = {'language': language}
    final = json.dumps(data,ensure_ascii=False).encode('utf8')
    return final



def updatePassword(email,code,password):

    em = selectUserID(email)
    code_old = selectCode(em)
    code_old = utils.remove_punctuation(str(code_old))

    if (code_old == code):

        query = "UPDATE user SET password = %s WHERE user_id = %s"
        data = (password,em)
        conn.run_query(query,data)


def insertCode(email,upload_at):

    user_id = selectUserID(email)

    if user_id == '':

        data = {'email': '0', 'code': '0'}
        final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
        return final
    else:

        em = selectUserID(email)

        code = selectCode(em)

        if code == '':

            code = utils.createCode()
            query = "INSERT INTO code_user (user_id, code, upload_at) VALUES (%s,%s,%s) ;"
            data = (em,code,upload_at)
            conn.run_query(query,data)
            data = {'email': email, 'code':code}
            final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
            mservice.sendEmail("qichwa@pucp.edu.pe","Qchw-2017",email, str(code)+" is your Quechua ASR verification code")
            return final
        else:

            code_old = selectCode(em)
            data = {'email': email, 'code': utils.remove_punctuation(str(code_old))}
            final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
            mservice.sendEmail("qichwa@pucp.edu.pe","Qchw-2017",email, utils.remove_punctuation(str(code_old))+" is your Quechua ASR verification code")
            return final


def selectCode(user_id):

    query = "SELECT code from code_user WHERE user_id = '%s';"
    data = (user_id)
    cursor = conn.run_query(query,data)
    code = ""

    for co in cursor:
        code = co

    return code

def insertUser_app(email,password,first_name,last_name,dni,phone,native_lang,region_id,provincia_id,distrito_id,created_at):

    em = selectUserID_app(email)
    d = selectDNI_app(dni)
    if (em == '' and d == ''):
        query = "INSERT INTO user_app (email,password,first_name,last_name,dni,phone,native_lang,region,provincia,distrito,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        data = (email,password,first_name,last_name,dni,phone,native_lang,region_id,provincia_id,distrito_id,created_at)
        conn.run_query(query,data)
        user_id = selectUserID_app(email)
        data = {'user_id': user_id ,'email': email, 'dni':dni, 'first_name':first_name, 'last_name': last_name}
        final = json.dumps(data,ensure_ascii=False).encode('utf8')
        return final
    else:
        data = {'user_id': '0' ,'email': '0', 'first_name':'0', 'last_name': '0'}
        final = json.dumps(data,ensure_ascii=False).encode('utf8')
        return final


def selectUserID_app(email):

    query = "SELECT user_app_id FROM user_app WHERE email = '%s' LIMIT 1;" %(email)
    data = ""
    cursor = conn.run_query(query,data)
    user_app_id = ""

    for user in cursor:
        user_app_id = user
    
    return user_app_id


def selectDNI_app(dni):
    query = "SELECT dni FROM user_app WHERE dni = '%s' LIMIT 1;" %(dni)
    data = ""
    cursor = conn.run_query(query,data)
    dni = ""

    for d in cursor:
        dni = d

    return dni


def login_app(email,password):

        query = "SELECT password,user_app_id, dni, first_name, last_name, native_lang FROM user_app WHERE email = '%s' LIMIT 1; " %(email)
        data = ""
        cursor = conn.run_query(query,data)

        c = 0
        user_app_id = ""
        first_name = ""
        last_name = ""
        dni = ""
        nl = ""

        for (password_bd, user, d, fname, lname, nls) in cursor:
                password_bd = str(password_bd)
                password_bd = re.sub('[%s]' % re.escape(string.punctuation),"", password_bd).lower()
                if password == password_bd:
                        c = 1
                        user_app_id = user
                        first_name = fname
                        last_name = lname
                        dni = d
                        nl = nls

        if c == 1:

		query = "SELECT count FROM audios_app WHERE user_app_id = '%s' LIMIT 1; " %(user_app_id)
                data = ""
                cursor = conn.run_query(query,data)
                count = ""
		for c in cursor:
			count = c

                data = {'user_app_id': user_app_id ,'email': email, 'dni': dni, 'first_name':first_name, 'last_name': last_name, 'lang':nl, 'count': count}
                final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
                return final
        else:

                data = {'user_app_id': '0' ,'email': '0', 'first_name':'0', 'last_name': '0'}
                final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
                return final

def selectUserEmail_app(email):

    em = selectUserID_app(email)

    if (em == ''):

        data = {'user_id': '0' ,'email': '0', 'first_name':'0', 'last_name': '0'}
        final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
        return final

    else:

        query = "SELECT user_app_id, dni, first_name, last_name FROM user_app WHERE user_app_id = %s LIMIT 1;"
        data = (em)
        cursor = conn.run_query(query,data)
        c = 0
        user_id = ""
        first_name = ""
        last_name = ""
        dni = ""

        for (user, d, fname,lname) in cursor:

            user_app_id = user
            first_name = fname
            last_name = lname
            dni = d

	query = "SELECT count FROM audios_app WHERE user_app_id = '%s' LIMIT 1; " %(em)
        data = ""
        cursor = conn.run_query(query,data)
        count = ""
        for c in cursor:
            count = c

        data = {'user_app_id': user_app_id, 'dni': dni, 'email': email, 'first_name':first_name, 'last_name': last_name,'count':count}
        final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
        return final


def getEmail(email):
    
    is_valid = validate_email(email,verify=True)
    em = selectUserID_app(email)
    if is_valid == True and em == '':
	return "Ok"
    else:
        return "No"


def getDNI(dni):
     url = "https://dni.optimizeperu.com/api/persons/"
     r = requests.get(url+dni)
     r.encoding = 'uft-8'
     print(r.text)
     final = json.dumps(r.text,ensure_ascii=False)
     print(final)
     return final

def getDialecto(ans):
     chanka = 0
     collao = 0
     dialecto = ""
     if ans[0] == 'a':
     	chanka += 1
     if ans[0] == 'b' or ans[0] == 'd':
     	collao += 1
     if ans[1] == 'a':
	chanka += 1
     if ans[1] == 'c':
        collao += 1
     if ans[2] == 'e':
        chanka += 1
     if ans[2] == 'b':
        collao += 1
     if ans[3] == 'a':
	chanka += 1
     if ans[3] == 'e':
 	collao += 1
     if ans[4] == 'b':
	chanka += 1
     if ans[4] == 'a':
	collao += 1
     print('Respuestas Chanka: ',chanka)
     print('Respuestas Collao: ',collao) 
     suma = chanka + collao
     print('La suma es: ',suma)
     if suma >= 4:
	if chanka > collao:
           print('chanca')
	   dialecto = "chanca"
        if collao > chanka:
	   print('collao')
	   dialecto = "collao"
	if chanka == collao:
	   dialecto = "chanca"
     data = {"dialecto":dialecto}
     final = json.dumps(data,ensure_ascii=False).encode('utf8')
     return final


def getEnglish(text):
    text = str(text)
    text = text.replace('í','i')
    text = text.replace('é','e')
    text = text.replace('á','a')
    text = text.replace('ú','u')
    text = text.replace('ó','o')
    return text


def getDialectoRegion(dep,pro,dis):
     data = pd.read_excel('dialecto.xls')
     data['Departamento'] = data['Departamento'].apply(getEnglish)
     data['Distrito'] = data['Distrito'].apply(getEnglish)
     df_mask=  data.query('Departamento == "'+dep+'" and Distrito == "'+dis+'"')
     dialecto = df_mask['Dialecto Quechua']
     ta = len(dialecto)
     dialect = ""
     print(dialecto)
     if ta == 0:
	dialect = "0"
     else:
	nmp=dialecto.to_numpy()
	nmp = str(nmp[0])
	if nmp == "Chanka":
	   dialect = "chanca"
	if nmp == "Cuzco-Collao":
	   dialect = "collao"
	if nmp == "0":
	   dialect = "0"
     data = {'dialecto': dialect}
     final = json.dumps(data,ensure_ascii=False).encode('utf8')
     return final	
