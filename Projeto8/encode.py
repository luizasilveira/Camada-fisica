from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import pickle

from scipy import signal
import soundfile as sf

def main():
    data, samplerate = sf.read("10convert.com_High-School-Musical-1-We-re-All-in-This-Together-Lyrics-1080pHD_iFu8Z-cV0Xk (online-audio-converter.com).wav")

    sinal = signalMeu()

    f =  44100

    audio = data[0:10*samplerate]

    dados = []
    for e in audio[:,0]:
        dados.append(e)

    t = np.linspace(0,10,len(dados))

    # 5a

    plt.plot(t,dados)
    plt.title("Audio original x Tempo")
    
    plt.show()

    sinal.plotFFT(dados,f)
    plt.show()

    # 5b

    dados = np.asarray(dados)

    normal = dados/max(dados)

    plt.plot(t,normal)
    plt.title("Audio normalizado x Tempo")
    
    plt.show()

    sinal.plotFFT(normal,f)
    plt.show()

    # 5c

    # exemplo de filtragem do sinal yAudioNormalizado

    # https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html

    nyq_rate = f/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = signal.kaiserord(ripple_db, width)
    cutoff_hz = 4000.0
    taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

    yFiltrado = signal.lfilter(taps, 1.0, normal)

    plt.plot(t,yFiltrado)
    plt.title("Audio passa baixa x Tempo")
    
    plt.show()

    sinal.plotFFT(yFiltrado,f)
    plt.show()

    # 5d

    t, s = sinal.generateSin(14000, 1, 10, f)

    modulado = yFiltrado*s

    plt.plot(t,modulado)
    plt.title("Audio modulado x Tempo")
    
    plt.show()

    sinal.plotFFT(modulado,f)
    plt.show()

    sf.write("save.wav", modulado, f)


if __name__ == "__main__":
    main()