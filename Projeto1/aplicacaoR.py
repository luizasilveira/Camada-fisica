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
serialName = "/dev/cu.usbmodem146201" # Mac    (variacao de)
#serialName = "COM5"                  # Windows(variacao de)
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
    

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    bufferReceived = bytearray()
    while True:
        rxBuffer, nRx = com.getData(1)
        bufferReceived += rxBuffer
        if (b"end" in bufferReceived):
            break
    
    imgSize = bufferReceived[:-3]
    rxBuffer, nRx = com.getData(int(imgSize))
    
    txLen = len(rxBuffer)

    
    
    with open("teste.jpg", "wb") as img:
        img.write(rxBuffer)

    print ("Recebidos {} bytes ".format(txLen))

    com.sendData(imgSize)
    print ("Transmitido {} bytes ".format(len(imgSize)))
    while(com.tx.getIsBussy()):
       pass
    

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()