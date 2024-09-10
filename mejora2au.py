# El código que proporcionó es un script de Python que incluye múltiples importaciones para diferentes
# bibliotecas/módulos, inicialización de variables globales y definiciones de funciones para grabar audio,
# transcribir el discurso y administrar el proceso de transcripción.

import threading  # para usar varios hilos al mismo tiempo
import sys        # para salir del programa
import datetime   # usar hora y fecha
import pyaudio    # grabación de audio
import wave       # generación de archivo de audio
import winsound   # producir sonido Beep de windows
import whisper    # reconocimiento automatico de voz
import time       # activar el sleep en segundos y (t/1000) para milisegundos
import msvcrt     # para esperar ENTER para continuar
import keyboard   # para utilizar las teclas del keyborad
import os.path    # para verificar si un archivos existe.

nombre_archivo = 'Texto_captura2.txt' # Nombre del archivo donde se guardaran las transcripciones

file_path = 'C:\Python\Repo_Chico\outputA1.wav' # ruta donde del primer archivo de audio 

n = 1  # número de la grabaciones REC A
l = 2  # número de la grabaciones REC B
m = 1  # número de fragmento analizado con whisper
total = 0  # número total de grabaciones
chico = 20  # tiempo de espera para obtener el primer archivo de audio .wav
infinity = 0  # variable para terminar programa


def REC_A():    # GRABACIÓN #####################################################
    """
    La función `Rec_A` registra la entrada de audio durante 15 segundos, la guarda en un archivo WAV e incrementa el
Número de grabación por 2.
    """

    global n  # comando para utlizar la variable global n desiganda para las grabaciones A

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
    """winsound.Beep(2000, 200)
    time.sleep(100/1000)
    winsound.Beep(2000, 200)"""

    fechaActual = datetime.datetime.now()
    fechaStrActual = datetime.datetime.strftime(
        fechaActual, '%d/%m/%Y %H:%M:%S')
    print(fechaStrActual + f" Grabando lado A número: {n}")

    seconds = 15    # tiempo de grabación en 10 segundos
    frames = []
    for i in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate

    # FINALIZANDO GRABACIÓN
    """winsound.Beep(500, 300)
    time.sleep(100/1000)
    winsound.Beep(500, 300)"""

    fechaActual = datetime.datetime.now()
    fechaStrActual = datetime.datetime.strftime(
        fechaActual, '%d/%m/%Y %H:%M:%S')
    print(fechaStrActual + f" Grabación lado A numero: {n} terminada.")

    # GENERACION DE ARCHIVO DE AUDIO
    obj = wave.open(f"outputA{n}.wav", "wb")
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))
    obj.close
    print(f"Archivo outputA_{n}.wav generado.")
    
    
    n += 2              # Incrementa en 2 el valor de n
    
    if keyboard.is_pressed('q'):    # si se presiona la letra q deja de grabar y llama a la funcion Whis_Infi()
        print("Dejando de grabar, se procede a solo transcribir..."+"\n")
        Whis_Infi()
        
    #time.sleep(chico)
    h3.start()

def REC_B():    # GRABACIÓN #####################################################

    global l  # comando para utlizar la variable global n desiganda para las grabaciones B

    time.sleep(10) # espera 10 segundos antes de grabar
    
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
    """winsound.Beep(2000, 200)
    time.sleep(100/1000)
    winsound.Beep(2000, 200)"""

    fechaActual = datetime.datetime.now()
    fechaStrActual = datetime.datetime.strftime(
        fechaActual, '%d/%m/%Y %H:%M:%S')
    print(fechaStrActual + f" Grabando lado A numero: {l}")

    seconds = 15    # tiempo de grabación en 10 segundos
    frames = []
    for i in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate

    # FINALIZANDO GRABACIÓN
    """winsound.Beep(500, 300)
    time.sleep(100/1000)
    winsound.Beep(500, 300)"""

    fechaActual = datetime.datetime.now()
    fechaStrActual = datetime.datetime.strftime(
        fechaActual, '%d/%m/%Y %H:%M:%S')
    print(fechaStrActual + f" Grabación lado A numero: {l} terminada.")

    # GENERACION DE ARCHIVO DE AUDIO
    obj = wave.open(f"outputA{l}.wav", "wb")
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))
    obj.close
    print(f"Archivo outputA_{l}.wav generado.")
    
    l += 2
    
    if keyboard.is_pressed('q'):
        print("Dejando de grabar, se procede a solo transcribir..."+"\n")
        Whis_Infi()


def Whis():  # WHISPER ##############################################################
    
    h1.join()
    h2.join()
    global chico  # la variable global chico desiganda para esperar los fragmentos de las grabaciones A
    global m  # la variable global m desiganda para analizar los fragmentos de las grabaciones A
    chico = 0
    
    if os.path.exists(file_path):

        fechaActual = datetime.datetime.now()
        fechaStrActual = datetime.datetime.strftime(
        fechaActual, '%d/%m/%Y %H:%M:%S')

        inicio = datetime.datetime.now()

        print(f"Analizando audio output{m}.wav")
        
        # CONFIGURACIÓN DEL MODULO WHISPER 'small' PARA RAPIDO, medium PARA PRECISIÓN, large PARA MAXIMA PRECISIÓN
        model = whisper.load_model('small')
        Texto = model.transcribe(f"outputA{m}.wav", language='Spanish', fp16=False)

        final = datetime.datetime.now()

        Tiempo = final - inicio

        print(f'Transcipción finalizada en {Tiempo.seconds} segundos'+"\n")
        print("''" + Texto["text"] + "''"+"\n")

        # Almacenado de texto en archivo Texto_captura2.txt
        
        with open(nombre_archivo, '+a') as archivo:
            archivo.write(fechaStrActual + f" Audio#{m} " + Texto["text"]+"\n")
        print("Texto agregado a Texto_captura2.txt")
        
        m += 1
        
        print(f"n = {n}"+"\n")
        print(f"l = {l}"+"\n")
        print(f"total = {total}"+"\n")
        print(f"m = {m}"+"\n")
        
    else:
        print('El archivo no existe')
        


def Whis_Infi():  # Blucle hasta terminar traduccion de todos los audios.#################################################

    h1.join()
    h2.join()
    h3.join()
    
    global m  # la variable global m desiganda para analizar los fragmentos de las grabaciones A
    #global n  # la variable global n desiganda para analizar los fragmentos de las grabaciones A
    #global l  # la variable global l desiganda para analizar los fragmentos de las grabaciones B
    global total  # la variable global total desiganda para contabilizar todas las grabaciones
    global infinity  # la variable global infiniti para terminar el programa
    
    if n > l:
        total = n
    else:
        total = l

    while m <= total:       # MIENTRAS 'm' SEA MENOR O IGUAL A 'total' SE TRANSCRIBIRAN LOS AUDIOS HASTA TERMINAR

        fechaActual = datetime.datetime.now()
        fechaStrActual = datetime.datetime.strftime(
            fechaActual, '%d/%m/%Y %H:%M:%S')
        inicio = datetime.datetime.now()
        print(f"Analizando audio output{m}.wav")

        # SELECCIÓN DE MODELO small PARA RAPIDO, medium PARA PRECISIÓN, large PARA MAXIMA PRECISIÖN
        model = whisper.load_model('small')
        Texto = model.transcribe(
            f"outputA{m}.wav", language='Spanish', fp16=False)
        final = datetime.datetime.now()

        Tiempo = final - inicio

        print(f'Transcipción finalizada en {Tiempo.seconds} segundos'+"\n")
        print("''" + Texto["text"] + "''"+"\n")

        with open(nombre_archivo, '+a') as archivo:
            archivo.write(fechaStrActual + f" Audio#{m} " + Texto["text"]+"\n")
        print("Texto agregado a Texto_captura2.txt")
        
        print(f"n = {n}"+"\n")
        print(f"l = {l}"+"\n")
        print(f"total = {total}"+"\n")
        print(f"m = {m}"+"\n")
              
        m += 1
        
    if m > total:
        print("Transcripción COMPLETADA en Texto_captura2.txt")
        infinity = 1
            

# MAIN ###################principal############################################
if __name__ == '__main__':
    
    # REC_A()
    # Whis()
    

    while infinity == 0:
        
        h1 = threading.Thread(name="REC_A", target=REC_A)
        h2 = threading.Thread(name="REC_B", target=REC_B)
        h3 = threading.Thread(name="Whis", target=Whis)

        h1.start()
        h2.start()
        #h3.start()

        #h1.join()
        #h2.join()
        #h3.join()

        

        # print("Presione la tecla ""q"" para detener el programa.")
        # time.sleep(3)
        # if keyboard.is_pressed('q'):
        # break

    print("Presione una tecla para continuar...")
    msvcrt.getch()
