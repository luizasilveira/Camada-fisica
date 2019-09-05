#!/usr/bin/env python3
# -- coding: utf-8 --
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################

print("comecou")

from enlace import *
import time



# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)
print("abriu com")

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

   

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega dados
    print ("gerando dados para transmissao :")
  
      #no exemplo estamos gerando uma lista de bytes ou dois bytes concatenados



    imagem = input("Nome do arquivo: ")
    
    
    with open(imagem, "rb") as image:
        f = image.read()
        imgBytes = bytearray(f)
        imgSize = bytes(str(len(imgBytes)), "UTF-8")
        txBuffer = imgSize + bytearray(b"end") + imgBytes
        #print(txBuffer)


    txLen = len(txBuffer)
    print(txLen)

    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))
    start = time.time()
    com.sendData(txBuffer)

    #espera o fim da transmissão
    while(com.tx.getIsBussy()):
       pass
    
    
    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()

    print ("Transmitido {} bytes ".format(txSize))

    rxBuffer2, nRx2 = com.getData(len(imgSize))
    if nRx2 == len(imgSize):
        print("Igual")
        end = time.time()

    delta = end - start
    taxa = len(imgBytes)/delta
    print("Tempo:             {} s".format(delta))
    print("Bytes por segundo: {} b/s".format(taxa))
    
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()