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
import math



# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM9"                  # Windows(variacao de)
print("abriu com")

def eop():

    eop = bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3])
    return eop 

def getFile():
    
    with open("image.png", "rb") as image:
        payload = image.read()
        payloadSize = bytes(str(len(payload)), "UTF-8")

    return payload

def eopReplaced():

    emptyPayload = bytes([0x00])*1

    eopReplaced = bytes([0x00]) + bytes([0xf1]) +  bytes([0x00]) + bytes([0xf2]) +  bytes([0x00]) + bytes([0xf3])

    emptyPayloadReplaced =  emptyPayload.replace(eop(), eopReplaced)
    payloadReplaced = getFile().replace(eop(), eopReplaced)

    return emptyPayloadReplaced, payloadReplaced

def allpayloads():
     eachPayloadmsg = [eopReplaced()[0][x:x+128] for x in range(0, len(eopReplaced()[0]), 128)]
     eachPayloadimg = [eopReplaced()[1][x:x+128] for x in range(0, len(eopReplaced()[1]), 128)]

     return eachPayloadmsg, eachPayloadimg
     
def totalPackage() : 
    total = len(allpayloads()[1])
    return total

def message1():
    serverNumber = bytes([0x93])
    totalPackage =  len(allpayloads()[1]).to_bytes(3,"little")
    # numberPackage = 0
    # emptyHead =  bytes([0x00]) * 3
    messageNumber = bytes([0x01])
    for payloadS in allpayloads()[0]:
        payloadSize = len(payloadS).to_bytes(1,"little")
    

    emptyhead = bytes([0x00])*4
    head = messageNumber + serverNumber +  totalPackage + payloadSize + emptyhead
    package = head + payloadS + eop()

    return package

def message5():
    messagetype = bytes([5])
    payloadSize = bytes([0])
    emptyHead = bytes([0])* 8

    head = messagetype + payloadSize + emptyHead
    package = head + eop()

    return package





def client():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")
   

    print ("gerando dados para transmissao :")

    # Transmite dado
    print("tentado transmitir .... {} bytes".format(len(message1())))

    inicia = False
    while not inicia:
        com.sendData(message1())
        print("Sent TYPE1")
        time.sleep(2)
      

        while(com.tx.getIsBussy()):
            pass

        head, headsize = com.getData(10,1)

        messageNumber = int.from_bytes(head[:1], "little")

        if messageNumber == 2:
            print("Received TYPE2")

            arquivo = getFile()
            arquivoSize = len(arquivo)

            totalPacotes = math.ceil(arquivoSize / 128)
            print(totalPacotes)
            print("kkk")
            pacoteAtual = 1
            com.rx.clearBuffer()
            while pacoteAtual <= totalPacotes:
                print ("pacote atual {}".format(pacoteAtual))
                payload = arquivo[(pacoteAtual - 1)*128 : pacoteAtual*128]

                head = bytes([3]) + pacoteAtual.to_bytes(3, "little") + totalPacotes.to_bytes(3, "little") + len(payload).to_bytes(1, "little") + bytes([0]) * 2
                message3 =  head + payload + eop()
                startTime = time.time()
                recebido = False
                while not recebido:
                    com.sendData(message3)
                    print(message3)
                    print(" ")
                    print("Sent TYPE3")

                    responseHead, responseSize = com.getData(10, 5)
                    print(responseHead, responseSize)
                    
                    if responseSize != 0:
                        
                        message_number = int.from_bytes(responseHead[:1], "little")
                        if message_number == 4:
                            print("Received TYPE4")
                            pacoteAtual +=1

                        if message_number == 7:
                            pacoteAtual = pacoteAtual    
                            

                        if message_number == 6:
                            print("Received TYPE6")
                            lastPackage = int.from_bytes(responseHead[1:4], "little")
                            print ("ultimo pacote recebido {}".format(lastPackage))
                            print("")
                            pacoteAtual = lastPackage + 1 
                            print ("pacote corrigido {}".format(pacoteAtual))

                        
                        recebido = True

                    if  time.time() - startTime > 20:
                        com.sendData(message5())
                        com.disable()
                        exit()
                    
                    com.rx.clearBuffer()         

                                
            

        else:
            inicia = False

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")

    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    client()