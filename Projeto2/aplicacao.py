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

def client():
   
    file = input("Nome do arquivo: ")
    
    with open(file, "rb") as file2:
        f = file2.read()
        f = bytes([0x00])*5 + bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3]) + bytes([0x00])*5 + bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3]) + bytes([0x00])*5
        payload = bytearray(f)
        print('teste3')
        
    #f = bytes([0x00])*5 + bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3]) + bytes([0x00])*5 + bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3]) + bytes([0x00])*5
    #payload = bytearray(f)
    #print('teste3')
            

    eop = bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3])
    eopReplaced = bytes([0x00]) + bytes([0xf1]) +  bytes([0x00]) + bytes([0xf2]) +  bytes([0x00]) + bytes([0xf3])
    
    payload = payload.replace(eop, eopReplaced)

    emptyHead = bytes([0x00]) * 6
    imgSize = len(payload).to_bytes(4,"big")
    head = imgSize + emptyHead
    print("teste")

    package = head + payload + eop
    print("teste2")

    OverHead = len(package)/len(payload)



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

    # Transmite dado
    print("tentado transmitir .... {} bytes".format(len(package)))
    start = time.time()
    com.sendData(package)

    #espera o fim da transmissão
    while(com.tx.getIsBussy()):
       pass

    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()

    print ("Transmitido {} bytes ".format(txSize))

    response, responseSize = com.getData(1)
    if responseSize == bytes([0xa3]):
        print("sucesso")

    end = time.time()
        

    delta = end - start
    ThroughPut = len(payload)/delta
    print("Tempo:      {} s".format(delta))
    print("ThroughPut: {} b/s".format(ThroughPut))
    print("OverHead:   {} b/s".format(OverHead))
    
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    client()