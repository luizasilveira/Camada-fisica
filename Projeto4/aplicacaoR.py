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
from datetime import datetime

def eop():
    
    eop = bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3])
    return eop 

def eopReplaced():

    emptyPayload = bytes([0x00])*1

    eopReplaced = bytes([0x00]) + bytes([0xf1]) +  bytes([0x00]) + bytes([0xf2]) +  bytes([0x00]) + bytes([0xf3])

    emptyPayloadReplaced =  emptyPayload.replace(eop(), eopReplaced)

    return emptyPayloadReplaced

def allpayloads():
     eachPayloadmsg = [eopReplaced()[x:x+128] for x in range(0, len(eopReplaced()), 128)]

     return eachPayloadmsg

def message2():

    messageNumber = bytes([0x02])

    for payloadS in allpayloads():
        payloadSize = len(payloadS).to_bytes(1,"little")
        print(payloadSize)

    emptyhead = bytes([0x00])*8
    head = messageNumber + payloadSize + emptyhead
    package = head + payloadS + eop()

    return package

def message4(numberPackage):
    msgType = bytes([4])
    numberPackageBytes = numberPackage.to_bytes(3, "little")
    payloadSize = bytes([0])
    emptyhead = bytes([0x00])*5

    head = msgType +  numberPackageBytes + payloadSize + emptyhead
    package = head + eop()

    return package

def message6(numberPackage):
    msgType = bytes([6])
    numberPackageBytes = numberPackage.to_bytes(3, "little")
    payloadSize = bytes([0])
    emptyhead = bytes([0x00])*5

    head = msgType +  numberPackageBytes + payloadSize + emptyhead
    package = head + eop()

    return package

def message5():
    msgType = bytes([5])
    payloadSize = bytes([0])
    emptyhead = bytes([0x00])*8

    head = msgType +  payloadSize + emptyhead
    package = head + eop()

    return package

    


def log(mensagem):
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(mensagem + " | " + dt_string)
    with open("server.log", "a") as file:
        file.write(mensagem + " | " + dt_string + "\n" + "\n")
        

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python3 -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/cu.usbmodem144201" # Mac    (variacao de)
serialName = "COM10"                  # Windows(variacao de)
print("abriu com")

def server():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

     # Log
    log("-------------------------")
    log("Comunicação inicializada")
    log("  porta : {}".format(com.fisica.name))
    log("-------------------------")
    
    # Faz a recepção dos dados
    log("Recebendo dados .... ")

    ocioso = False
    bufferReceived = bytearray()
    while not ocioso:
        head, headSize = com.getData(10,1)
       

        if headSize != 0:
            log("TIPO 1 recebido")

            serverNumber = 147

            messageNumber = int.from_bytes(head[:1], "little")
            log("Numero da mensagem {}".format(messageNumber))

            serverNumberR = int.from_bytes(head[1:2], "little")
            log("Numero do Servidor {}".format(serverNumberR))

            totalPackage = int.from_bytes(head[2:5], "little")
            log("Numero total de pacotes {}".format(totalPackage))

            payloadSize = int.from_bytes(head[5:6], "little")
            log ("Tamnaho do payload {}".format(payloadSize))
            print(" ")
            
            if serverNumberR == serverNumber:
                log("Numero do servidor correto")
                com.sendData(message2())

                log("TIPO 2 Transmitido")

                tudo = bytes()

                cont = 1
                com.rx.clearBuffer()
                while cont <= totalPackage:
                    recebido = False
                    startTime = time.time()
                    while not recebido:
                        response = False
                        head, headSize = com.getData(10,2)
                        print(" ")
                        if headSize != 0:
                            

                            msgType = int.from_bytes(head[:1], "little")
                            numberPackage = int.from_bytes(head[1:4], "little")
                            
                            payloadSize = int.from_bytes(head[7:8], "little")
                        

                            if msgType == 3:
                                log("TIPO 3 recebido")
                                log("Numero do pacote recebido: {}".format(numberPackage))
                                if numberPackage == cont:
                                    log("Número do pacote esperado!!")
                                    print(" ")
                                    payloadEop, payloadEopSize = com.getData(payloadSize + len(eop()),1)
                                    
                                   

                                    if payloadSize != payloadEopSize - len(eop()) and not response:
                                        log("ERRO: Tamanho do payload errado.")
                                        com.sendData(message6(numberPackage))
                                        response = True
                                        log("TIPO 6 Transmitido")
                                        print(" ")

                                    if eop() in payloadEop:
                                        i = payloadEop.find(eop())
                                        log("EOP na posicão {}".format(i))
                                        payload = payloadEop[:i]

                                        leftover = payloadEop[i:]
                                        if leftover == eop() and not response:
                                            log("EOP está no lugar certo")
                                            response = True
                                            log("TIPO 4 Transmitido")
                                           
                                            tudo += payload
                                            com.sendData(message4(numberPackage))
                                            cont += 1
                                            recebido = True
                                            
                                            
                                            log ("Proximo pacote esperado : {}".format(cont))
                                            
                                            continue
                                           
                                        else:
                                            log("ERRO: EOP está no lugar errado")
                                            com.sendData(message6(numberPackage))
                                            log("TIPO 6 Transmitido")
                                            response = True
                                    else:
                                        log("ERRO: EOP não encontrado")
                                        com.sendData(message6(cont))
                                        log("TIPO 6 Transmitido")
                                        response = True
                                else:
                                    log("ERRO: Número do pacote diferente do esperado")
                                    com.sendData(message6(cont))
                                    log("TIPO 6 Transmitido")
                                    response = True
                        
                        time.sleep(1)
                        if time.time() - startTime > 20 and not response:
                            response = True
                            com.sendData(message5())
                            log("TIPO 5 Transmitido")
                            log("Time out")
                            com.disable()
                            exit()
                        
                        
                            
                        com.rx.clearBuffer()

                        
                with open("testeee.jpg", "wb") as img:
                    img.write(tudo)
        
                com.disable()
                exit()

        com.rx.clearBuffer()    
        ocioso = False 


    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    server()