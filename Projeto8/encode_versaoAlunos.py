

#importe as bibliotecas

from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import pickle

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100

    freq = 44100
    signal = signalMeu()
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    duration = 2 #tempo em segundos que ira emitir o sinal acustico 
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3

    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 

    tabela_DTMF = {"1":[1209, 697], "2":[1336, 697], "3":[1477, 697], "A":[1633, 697],
         "4":[1209, 770], "5":[1336, 770], "6":[1477, 770], "B":[1633, 770],
         "7":[1209, 852], "8":[1336, 852], "9":[1477, 852], "C":[1633, 852],
         "X":[1209, 941], "0":[1336, 941], "#":[1477, 941], "D":[1633, 941]}

    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    NUM = input("Número de 0 a 9: ") 
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    
    while NUM not in tabela_DTMF:
        print("{} não está nesse intervalo.".format(NUM))
        NUM = input("Número de 0 a 9: ")
        print("Gerando Tom referente ao símbolo : {}".format(NUM))
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides

    time1, signaX = signal.generateSin(tabela_DTMF[NUM][0], gainX, duration, freq)
    time2, signaY = signal.generateSin(tabela_DTMF[NUM][1], gainY, duration, freq)

    signalTotal=[]
    for i in range(len(signaX)):
        signalTotal.append(signaX[i]+signaY[i])
    
    #printe o grafico no tempo do sinal a ser reproduzido
    # reproduz o som
    sd.play(signalTotal, freq)
    
    # Exibe gráficos
    plt.plot(time1, signalTotal)
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.title("Soma das senoides")
    plt.axis([0, 0.05, -0.8, 0.8])
    plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()
