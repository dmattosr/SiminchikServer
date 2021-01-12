# -*- coding: utf-8 -*-
import sys
import re, string
import urllib2
import demjson
import json
import generaldao as gdao
import connectiondb as conn
import model

reload(sys)
sys.setdefaultencoding('Cp1252')


def insertAudio(email,name,url,upload_at):

    user_id = gdao.selectUserID(email)

    query = "INSERT INTO audio (user_id,name,url,upload_at) VALUES (%s,%s,%s,%s)"
    data = (user_id,name,url,upload_at)
    conn.run_query(query,data)
    data = {'email': email ,'upload_at': upload_at, 'name':name}
    final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
    print upload_at+name
    return final


def selectAudio(name,path):
    print "SA1"
    result = model.run(path+"/"+name)
    print "SA2"
    query = "SELECT phrase_id, upload_at FROM audio WHERE name = '"+name+"' LIMIT 1;"
    data = ""
    cursor = conn.run_query(query,data)
    phrase_id = ""
    upload_at = ""
    for (phrase, date_audio) in cursor:

        phrase_id = str(phrase)
        upload_at = date_audio

    #insertPhrases(users_id,'quz','esp','txt',result,result,0,upload_at)

    query = "SELECT user_id, text_source, text_target FROM phrase  WHERE phrase_id = '"+phrase_id+"' LIMIT 1;"
    cursor = conn.run_query(query,data)
    text_source = ""
    text_target = ""
    user_id = ""
    for (u, q, s) in cursor:
        user_id = u
        text_source = q
        text_target = s

   #data = {'user_id': user_id ,'upload_at': upload_at, 'name':name,'text_source':text_source,'text_target':text_target}
    data = {'user_id': "1" ,'upload_at': "22-02-18", 'name':"hispana.wav",'text_source':result,'text_target':result}
    final = final = json.dumps(data,ensure_ascii=False).encode('utf8')
    return final


def insertPhrases(user_id,source,target,format,text_source,text_target,like_flag,upload_at):

    query = "INSERT INTO phrase (user_id,source,target,format,text_source,text_target,like_flag,upload_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (user_id,source,target,format,text_source,text_target,0,upload_at)
    conn.run_query(query,data)


def selectPhrases(email):

    em = gdao.selectUserID(email)

    query = "SELECT phrase_id, text_source, text_target, like_flag, upload_at FROM phrase WHERE user_id = %s ;" %(em)
    data = ""
    cursor = conn.run_query(query,data)
    ii = []
    tq = []
    tsp = []
    lf = []
    dup = []
    jphrases = []
    for (pid, text_source, text_target, like_flag, upload_at) in cursor:
        ii.append(pid)
        tp.append(text_source)
        tsp.append(text_target)
        lf.append(like_flag)
        dup.append(upload_at)

    i = 0
    for a in ii:

        jphrases.append({'phrase_id':str(ii[i]),'text_source':tq[i],'text_target': tsp[i],'like_flag':str(lf[i]),'upload_at':dup[i]})
        i = i + 1

    data = {'email': email,'phrases':jphrases}
    final = json.dumps(data,ensure_ascii=False).encode('utf8')
    return final


def updatePhrases(email,text_source,like_flag):

    em = gdao.selectUserID(email)

    query = "UPDATE phrase SET like_flag = %s WHERE text_source = %s AND user_id = %s"
    data = (like_flag,text_source,em)
    conn.run_query(query,data)


def selectConfig(email):

    user_id = gdao.selectUserId(email)

    query = "SELECT parameter, descu FROM config WHERE user_id = %s ;" %(user_id)
    data = ""
    cursor = conn.run_query(query,data)

    p = []
    d = []
    config = []
    for (param, desc) in cursor:

        p.append(param)
        l.append(desc)

    i = 0
    for a in p:

        config.append({'parameter':p[i],'descu':str(l[i])})
        i = i + 1

    data = {'email': email,'config':config}
    final = json.dumps(data,ensure_ascii=False).encode('utf8')
    return final


def updateConfig(email,parameter,descu):

    user_id = gdao.selectUserId(email)

    query = "UPDATE config SET parameter = %s, descu = %s WHERE user_id = %s"
    data = (param,desc,user_id)
    conn.run_query(query,data)


def selectUserIdDNI_app(dni):

    query = "SELECT user_app_id FROM user_app WHERE dni = '%s' LIMIT 1;" %(dni)
    data = ""
    cursor = conn.run_query(query,data)
    user_app_id = ""

    for user in cursor:
        user_app_id = user
    
    return user_app_id

def select_text1():
    query = "SELECT text_id FROM prompts_names"
    data = ""
    cursor = conn.run_query(query,data)
    text_ids = []
    for text in cursor:
        text_ids.append(text)
    data = {'text': text_ids}
    final = json.dumps(data,ensure_ascii=False).encode('utf8')
    return final

def select_text(lang):

    query = "SELECT id, text FROM text_prompt WHERE status = 0 and type_lang = %s;" %(lang)
    data = ""
    cursor = conn.run_query(query,data)

    country_id = []
    name = []

    for (ids, texts) in cursor:

        country_id.append(ids)
        name.append(texts)

    i = 0

    country = []

    for a in country_id:
        
        p = {'id':country_id[i],'text':name[i]}
        country.append(p)
        i = i + 1

    data = {'text_prompts': country}
    final = json.dumps(data,ensure_ascii=False).encode('utf8')
    return final

def record_audio(filename,date):

    filenames = filename.split('_')
    number_id = filenames[2].split('.')
    user_app_id = selectUserIdDNI_app(filenames[0])
    print user_app_id
    print filenames[0]
    query = "SELECT user_app_id,count FROM audios_app WHERE user_app_id = '%s' LIMIT 1;" %(user_app_id)
    data = ""
    cursor = conn.run_query(query,data)
    user_app_test_id = ""
    count = 1
    for user,c in cursor:
        user_app_test_id = user
        count = c + 1
    query = "UPDATE text_prompt SET status = %s WHERE id = %s"
    data = (1,int(number_id[0]))
    conn.run_query(query,data)
    if user_app_test_id == '':

        query = "INSERT INTO audios_app (user_app_id,date,status) VALUES (%s,%s,%s)"
        data = (user_app_id,date,1)
        conn.run_query(query,data)
        print "3"
    else:
        query = "UPDATE audios_app SET count = %s, date = %s WHERE user_app_id = %s"
        data = (count,date,user_app_id)
        conn.run_query(query,data)
        print "4"

    datas = {'user_app_id': user_app_id, 'filename':filename, 'upload_at': date}
    final = final = json.dumps(datas,ensure_ascii=False).encode('utf8')
    return final
