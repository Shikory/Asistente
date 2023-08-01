import threading
import datetime  # usar hora y fecha
import pyaudio  # grabación de audio
import wave     # generación de archivo de audio
import winsound  # producir sonido Beep de windows
import time     # activar el sleep en segundos y (t/1000) para milisegundos
import msvcrt   # para esperar ENTER para continuar


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
    print(fechaStrActual + " Grabando lado A.")

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
    print(fechaStrActual + " Grabación lado A terminada.")

    # GENERACION DE ARCHIVO DE AUDIO
    obj = wave.open("outputA.wav", "wb")
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))
    obj.close
    print("Archivo outputA.wav generado.")

def REC_B():    # GRABACIÓN #####################################################

    time.sleep(5)
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
    print(fechaStrActual + " Grabando lado B")

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
    print(fechaStrActual + " Grabación lado B terminada.")

    # GENERACION DE ARCHIVO DE AUDIO
    obj = wave.open("outputB.wav", "wb")
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))
    obj.close
    print("Archivo outputB.wav generado.")




# MAIN ###################principal############################################
if __name__ == '__main__':
    # REC_A()
    # Whis()
    h1 = threading.Thread(name="REC_A", target=REC_A)
    h2 = threading.Thread(name="REC_A", target=REC_B)
        
    h1.start()
    h2.start()

    h1.join()
    h2.join()
    
    print("Presione una tecla para continuar...")
    msvcrt.getch()
