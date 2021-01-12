import os
import librosa

def run(audio):
        print "name audio: "+audio
        #name_audio = audio.split("/")
        os.system("ffmpeg -i '"+audio+"' -acodec pcm_s16le -ac 1 -ar 16000 prueba.wav")
	os.system("deepspeech --model output_graph.pb --alphabet quz_alphabet.txt --audio prueba.wav >> result.txt")
	archivo = open("result.txt", "r") 
	contenido = archivo.read()
	os.system("rm result.txt")
        os.system("rm prueba.wav")
	return contenido
