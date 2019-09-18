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

def message4s(numberPackage):
    msgType = bytes([7])
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
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")
    
    # Faz a recepção dos dados
    print ("Recebendo dados .... ")

    ocioso = False
    bufferReceived = bytearray()
    while not ocioso:
        head, headSize = com.getData(10,1)
        print(head)

        if headSize != 0:
            print("Received TYPE1")

            serverNumber = 147

            messageNumber = int.from_bytes(head[:1], "little")
            print ("Numero da mensagem {}".format(messageNumber))

            serverNumberR = int.from_bytes(head[1:2], "little")
            print ("Numero do Servidor {}".format(serverNumberR))

            totalPackage = int.from_bytes(head[2:5], "little")
            print ("Numero total de pacotes {}".format(totalPackage))

            payloadSize = int.from_bytes(head[5:6], "little")
            print ("Tamnaho do payload {}".format(payloadSize))
            
            if serverNumberR == serverNumber:
                com.sendData(message2())

                print("Sent TYPE2")

                tudo = bytes()

                cont = 1
                print ("cont {}".format(cont))
                com.rx.clearBuffer()
                while cont <= totalPackage:
                    print("Entrou")
                    recebido = False
                    startTime = time.time()
                    while not recebido:
                        head, headSize = com.getData(10,2)
                        print("get data1")
                        if headSize != 0:
                            

                            msgType = int.from_bytes(head[:1], "little")
                            numberPackage = int.from_bytes(head[1:4], "little")
                            
                            payloadSize = int.from_bytes(head[7:8], "little")
                        

                            if msgType == 3:
                                print("Received TYPE3")
                                print ("numero do pacote recebido {}".format(numberPackage))
                                if numberPackage == cont:
                                    print("Número do pacote esperado")
                                    payloadEop, payloadEopSize = com.getData(payloadSize + len(eop()),1)
                                    print("getdata 2")
                                   

                                    if payloadSize != payloadEopSize - len(eop()):
                                        print("ERRO: Tamanho do payload errado.")
                                        com.sendData(message6(numberPackage))
                                        print("Sent TYPE6")

                                    if eop() in payloadEop:
                                        i = payloadEop.find(eop())
                                        print("EOP na posicão {}".format(i))
                                        payload = payloadEop[:i]

                                        leftover = payloadEop[i:]
                                        if leftover == eop():
                                            print("EOP está no lugar certo")
                                            print("Sent TYPE4")
                                            print(" ")
                                            tudo += payload
                                            com.sendData(message4(numberPackage))
                                            cont += 1
                                            recebido = True
                                            
                                            
                                            print ("Proximo pacote esperado : {}".format(cont))
                                            print(" ")
                                            continue
                                           
                                        else:
                                            print("ERRO: EOP está no lugar errado")
                                            com.sendData(message6(numberPackage))
                                            print("Sent TYPE6")
                                    else:
                                        print("ERRO: EOP não encontrado")
                                        com.sendData(message6(numberPackage))
                                        print("Sent TYPE6")
                                else:
                                    print("ERRO: Número do pacote diferente do esperado")
                                    com.sendData(message6(numberPackage))
                                    print("Sent TYPE6")

                        if time.time() - startTime > 20:
                            com.sendData(message5())
                            print("Sent TYPE5")
                            print("Time out")
                            com.disable()
                            exit()

                        if time.time() - startTime > 10:
                            com.sendData(message4(cont))
                            print("Sent TYPE44")
                            print(" ")
                       
                        

                        

                        com.rx.clearBuffer()

                           

                
                print("saiu")
                with open("testeee.jpg", "wb") as img:
                    img.write(tudo)
        


        com.rx.clearBuffer()    
        ocioso = False 

#        # payload = payload.replace(eopReplaced, eop)

        # payloadSize = len(payload)

        # sizeReceived = payloadEopSize - len(eop)

        # if sizeReceived == payloadSize:
        #     print("Sucesso")
        #     com.sendData(bytes([0xa3]))
        #     print ("Transmitido {} bytes ".format(1))
    
        # print ("Recebidos {} bytes ".format(headSize + payloadEopSize))
        # print(" ")

        # if packageNumber == totalPackage:
        #     with open("testeee.jpg", "wb") as img:
        #         img.write(bufferReceived)
        #     # stop = True

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    server()