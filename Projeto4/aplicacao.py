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
     eachPayloadmsg = [eopReplaced()[0][x:x+128] for x in range(0, len(eopReplaced()), 128)]
     eachPayloadimg = [eopReplaced()[1][x:x+128] for x in range(0, len(eopReplaced()), 128)]

     return eachPayloadmsg, eachPayloadimg


def message1():
    serverNumber = bytes([0x93])
    totalPackage = len(allpayloads()[0]).to_bytes(3,"little")
    # numberPackage = 0
    # emptyHead =  bytes([0x00]) * 3
    messageNumber = bytes([0x01])
    for payloadS in allpayloads()[0]:
        payloadSize = len(payloadS).to_bytes(1,"little")
        print(payloadSize)

    emptyhead = bytes([0x00])*4
    head = messageNumber + serverNumber + totalPackage + payloadSize + emptyhead
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
    start = time.time()
    com.sendData(message1())

    #espera o fim da transmissão
    while(com.tx.getIsBussy()):
        pass

    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()

    print ("Transmitido {} bytes ".format(txSize))

        # response, responseSize = com.getData(1)

        # if response == bytes([0xa1]):
        #     print("ERRO: EOP não encontrado")
        # if response == bytes([0xa2]):
        #     print("ERRO: EOP está no lugar errado")
        # if response == bytes([0xa3]):
        #     print("Sucesso")
    
        # end = time.time()
            

        # delta = end - start
        # ThroughPut = len(payload)/delta
        # OverHead = len(package)/len(payload)

        # print("Tempo:      {} s".format(delta))
        # print("ThroughPut: {} b/s".format(ThroughPut))
        # print("OverHead:   {} %".format(OverHead))
        # print(" ")
         
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")

    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    client()