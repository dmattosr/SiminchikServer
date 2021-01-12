from time import gmtime, strftime
from random import randint
import re, string, os
import random

UPLOAD_FOLDER = '/home/usuario/Escritorio/app/audio'
ALLOWED_EXTENSIONS = set(['wav', 'ogg', 'mp', 'mp3', 'mp4'])
CHANCA_AUDIOS = '/home/ubuntu/app_final/app_test/chanca'

def getAudio(url):
    list_audio = os.listdir(url)
    return random.choice(list_audio)


def createFile():

    timer = strftime("%d-%m-%Y", gmtime())
    date = timer.replace("-","_")
    return date

def allowed_file(filename):

    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def createCode():

	return randint(1000, 9999)


def remove_punctuation ( text ):
    return re.sub('[%s]' % re.escape(string.punctuation), '', text.replace("L",""))
