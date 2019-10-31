from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import pickle

from scipy import signal
import soundfile as sf

def main():
    data, samplerate = sf.read("save.wav")

    sinal = signalMeu()

    f =  44100

    dados = data

    t = np.linspace(0,10,len(dados))

    plt.plot(t,dados)
    plt.title("Audio recebido x Tempo")
    
    plt.show()

    sinal.plotFFT(dados,f)
    plt.show()


    # desmodulando

    t, s = sinal.generateSin(14000, 1, 10, f)

    desmodulado = dados*s

    plt.plot(t,desmodulado)
    plt.title("Audio desmodulado x Tempo")
    
    plt.show()

    sinal.plotFFT(desmodulado,f)
    plt.show()

    # filtro

    nyq_rate = f/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = signal.kaiserord(ripple_db, width)
    cutoff_hz = 4000.0
    taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

    yFiltrado = signal.lfilter(taps, 1.0, desmodulado)

    plt.plot(t,yFiltrado)
    plt.title("Audio passa baixa x Tempo")
    
    plt.show()

    sinal.plotFFT(yFiltrado,f)
    plt.show()

    sd.play(yFiltrado)
    sd.wait()

if __name__ == "__main__":
    main()