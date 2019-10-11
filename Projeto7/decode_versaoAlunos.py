#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
from suaBibSignal import signalMeu
import time
import peakutils
from peakutils.plot import plot as pplot


#funcao para transformar intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    signal = signalMeu()
    freqDeAmostragem = 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = freqDeAmostragem  #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 1 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    n = 1
    print("A captaçao comecara em {} segundos ".format(n))
    time.sleep(n)
    #use um time.sleep para a espera
    #faca um print informando que a gravacao foi inicializada
    print("A gravaçao foi inicializada")
   
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    numAmostras =  freqDeAmostragem * duration
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
   
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    dados = []
    for e in audio[:,0]:
        dados.append(e)
        
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!

    t = np.linspace(0,duration,int(numAmostras))
    print(len(dados))
    print(len(t))

    #plot do gravico  áudio vs tempo!
    plt.plot(dados,t)
    plt.grid()
    plt.title('audio vs tempo')
    plt.show()
   
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias

    xf, yf = signal.calcFFT(dados, freqDeAmostragem)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.show()
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    #index = peakutils.indexes(,,)
    index = peakutils.indexes(yf, thres=0.5, min_dist=15)
    print(index)
    
    #printe os picos encontrados! 
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
        #plt.show()

if __name__ == "__main__":
    main()
