import threading
import datetime  # usar hora y fecha
import pyaudio  # grabación de audio
import wave     # generación de archivo de audio
import whisper  # reconocimiento automatico de voz
import winsound  # producir sonido Beep de windows
import time     # activar el sleep
import msvcrt   # para esperar ENTER para continuar
# biblioteca de conversión de texto a voz en Python. A diferencia de las bibliotecas alternativas, funciona sin conexión y es compatible con Python 2 y 3.
import pyttsx3


# nombre del archivo donde se guardaran las transcripciones
nombre_archivo = 'Texto_captura.txt'
# nombre de la variable que habla las transcripciones
Oido = " "

# editando configuración por defecto de la voz que repetira las instrucciones
"""engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

engine.setProperty('rate', 178)  # 178
engine.setProperty('volume', 0.8)"""


def REC_A():    # GRABACIÓN #####################################################
    # CONFIGURACIÓN DEL ARCHIVO DE GRABACIÓN
    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    # INICIANDO GRABACIÓN
    winsound.Beep(2000, 200)
    time.sleep(100/1000)
    winsound.Beep(2000, 200)

    fechaActual = datetime.datetime.now()
    fechaStrActual = datetime.datetime.strftime(
        fechaActual, '%d/%m/%Y %H:%M:%S')
    print(fechaStrActual + " Grabando...")

    seconds = 10    # tiempo de grabación en 10 segundos
    frames = []
    for i in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate

    # FINALIZANDO GRABACIÓN
    winsound.Beep(500, 300)
    time.sleep(100/1000)
    winsound.Beep(500, 300)

    fechaActual = datetime.datetime.now()
    fechaStrActual = datetime.datetime.strftime(
        fechaActual, '%d/%m/%Y %H:%M:%S')
    print(fechaStrActual + " Grabación terminada.")

    # GENERACION DE ARCHIVO DE AUDIO
    obj = wave.open("output.wav", "wb")
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))
    obj.close
    print("Archivo output.wav generado.")


def Whis():  # WHISPER ##############################################################

    global Oido  # comando para utlizar la variable global Oido desiganda para que la computadora hable

    fechaActual = datetime.datetime.now()
    fechaStrActual = datetime.datetime.strftime(
        fechaActual, '%d/%m/%Y %H:%M:%S')

    inicio = datetime.datetime.now()

    print("Analizando audio output.wav")
    # SELECCIÓN DE MODELO small PARA RAPICO Y medium PARA PRESICION
    model = whisper.load_model('medium')

    Texto = model.transcribe("output.wav", language='Spanish', fp16=False)

    Oido = Texto["text"]

    final = datetime.datetime.now()

    Tiempo = final - inicio

    print(f'Transcipción finalizada en {Tiempo.seconds} segundos'+"\n")
    print("''" + Texto["text"] + "''"+"\n")

    with open(nombre_archivo, '+a') as archivo:
        archivo.write(fechaStrActual + Texto["text"]+"\n")
    print("Archivo Texto_captura.txt generado.")

    # codigo para hacer hablar la computadora
    engine = pyttsx3.init()
    engine.say(Oido)
    engine.runAndWait()
    engine.stop()
    Oido = " "
    print("Hablando...")


# MAIN ###################principal############################################
if __name__ == '__main__':
    # REC_A()
    # Whis()
    h1 = threading.Thread(name="REC_A", target=REC_A)
    h2 = threading.Thread(name="Whisper", target=Whis)

    h1.start()
    h2.start()

    h1.join()
    h2.join()

    print("Presione una tecla para continuar...")
    msvcrt.getch()
