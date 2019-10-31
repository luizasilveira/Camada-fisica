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
    sd.default.channels = 1  #voce pode ter que alterar isso dependendo da sua placa
    duration = 2 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


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
    #printe os picos encontrados! 
    index = peakutils.indexes(yf, thres=0.1, min_dist=50)
    picos = [xf[i] for i in index if xf[i] > 600 and xf[i] < 1800]
    maxi = max(picos, key=int)
    minn = min(picos, key=int)
    delta = 10
    print("Picos : {}  ".format(picos))

    tabela_DTMF = {"1":[1209, 697], "2":[1336, 697], "3":[1477, 697], "A":[1633, 697],
         "4":[1209, 770], "5":[1336, 770], "6":[1477, 770], "B":[1633, 770],
         "7":[1209, 852], "8":[1336, 852], "9":[1477, 852], "C":[1633, 852],
         "X":[1209, 941], "0":[1336, 941], "#":[1477, 941], "D":[1633, 941]}

    if 1209 + delta >= maxi >= 1209 - delta :
        if 697 + delta >= minn >= 697 - delta:     
            print("A tecla encontrada foi a : 1  ")  

    if 1336 + delta >= maxi >= 1336 - delta:
        if 697 + delta >= minn >= 697 - delta:   
            print("A tecla encontrada foi a : 2  ")  

    if 1477 + delta >=  maxi >= 1477 - delta:
        if 697 + delta >= minn >= 697 - delta :   
            print("A tecla encontrada foi a : 3  ")  


    if 1633 + delta >= maxi >= 1633 - delta:
        if 697 + delta >= minn >= 697 - delta :   
            print("A tecla encontrada foi a : A  ")  

    if 1209 + delta >= maxi >= 1209 - delta :
        if 770 + delta >= minn >= 770 - delta :   
            print("A tecla encontrada foi a : 4  ")  

    if 1336 + delta >= maxi >= 1336 - delta :
        if 770 + delta >= minn >= 770 - delta:   
            print("A tecla encontrada foi a : 5  ")    

    if 1477 + delta >= maxi >= 1477 - delta: 
        if 770 + delta >= minn >= 770 - delta:   
            print("A tecla encontrada foi a : 6  ")    

    if 1633 + delta >= maxi >= 1633 - delta:
        if 770 + delta >= minn >= 770 - delta :   
            print("A tecla encontrada foi a : B  ")    

    if 1209 + delta >= maxi >= 1209 - delta:
        if 852 + delta >= minn >= 852 - delta :   
            print("A tecla encontrada foi a : 7  ")

    if 1336 + delta >= maxi >= 1336 - delta:
        if 852 + delta >= minn >= 852 - delta :   
            print("A tecla encontrada foi a : 8  ")

    if 1477 + delta >= maxi >= 1477 - delta :
        if 852 + delta >= minn >= 852 - delta :   
            print("A tecla encontrada foi a : 9  ")    
    if 1633 + delta >= maxi >= 1633 - delta :
        if 852 + delta >= minn >= 852 - delta :   
            print("A tecla encontrada foi a : C  ")    

    
    if 1209 + delta  >= maxi >= 1209 - delta :
        if 941 + delta >= minn >= 941 - delta  :   
            print("A tecla encontrada foi a : X  ")  
    if 1336 + delta  >= maxi >= 1336 - delta:
        if 941 + delta >= minn >= 941 - delta :   
            print("A tecla encontrada foi a : 0  ")        
    if 1477 + delta  >= maxi >= 1477 - delta:
        if 941 + delta >= minn >= 941 - delta  :   
            print("A tecla encontrada foi a : #  ")    
    if 1633 + delta >= maxi >= 1633 - delta:
        if 941 + delta >= minn >= 941 - delta  :   
            print("A tecla encontrada foi a : D  ")    


    
    
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
        #plt.show()

if __name__ == "__main__":
    main()
