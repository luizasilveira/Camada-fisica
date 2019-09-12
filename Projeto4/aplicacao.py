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
serialName = "COM3"                  # Windows(variacao de)
print("abriu com")

def eop():

    eop = bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3])
    return eop 

def payload():
    
    with open("image.png", "rb") as image:
        payload = image.read()
        payloadSize = bytes(str(len(payload)), "UTF-8")

    return payload

def eopReplaced():

    emptyPayload = bytes([0x00])*1

    eopReplaced = bytes([0x00]) + bytes([0xf1]) +  bytes([0x00]) + bytes([0xf2]) +  bytes([0x00]) + bytes([0xf3])

    emptyPayloadReplaced =  emptyPayload.replace(eop(), eopReplaced)
    payloadReplaced = payload().replace(eop(), eopReplaced)

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
    head = messageNumber + serverNumber +  totalPackage() + payloadSize + emptyhead
    package = head + payloadS + eop()

    return package

def message3():
    serverNumber = bytes([0x93])
    totalPackage = len(allpayloads()[1]).to_bytes(3,"little")
    numberPackage = 0
    # numberPackage = 0
    # emptyHead =  bytes([0x00]) * 3
    messageNumber = bytes([0x03])
    for payloadS in allpayloads()[1]:
        payloadSize = len(payloadS).to_bytes(1,"little")
        numberPackage += 1
        numberPackageB = numberPackage.to_bytes(3,"little")
    

    emptyhead = bytes([0x00])*2
    head = messageNumber + numberPackageB + totalPackage + payloadSize + emptyhead
    package = head + payloadS + eop()

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
    while not inicia :

        start = time.time()
        com.sendData(message1())

        #espera o fim da transmissão
        while(com.tx.getIsBussy()):
            pass

        # Atualiza dados da transmissão
        txSize = com.tx.getStatus()

        print ("Transmitido {} bytes ".format(txSize))
        time.sleep(5)

        head, headsize = com.getData(10)
        messageNumber = int.from_bytes(head[:1], "little")
        print ("Numero da mensagem : {}".format(messageNumber))

        if messageNumber == 2:
            cont = 1
            print("esta certo")
            while cont <= totalPackage():
                com.sendData(message3())
                time1 = time.time()
                com.getData(10)
                head, headsize = com.getData(10)
                messageNumber = int.from_bytes(head[:1], "little")
                if messageNumber == 4:
                    cont += 1
                if messageNumber == 6:
                    print("n sei")

            timer2 = time.time()

            

        else:
            inicia = False

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")

    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    client()