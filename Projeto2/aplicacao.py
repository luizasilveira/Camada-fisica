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
   
    #file = input("Nome do arquivo: ")
    
    # with open(file, "rb") as file2:
    #     f = file2.read()
    #     f = bytes([0x00])*5 + bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3]) + bytes([0x00])*5 + bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3]) + bytes([0x00])*5
    #     payload = bytearray(f)
    #     print('teste3')
        
    f = bytes([0x00])*40 + bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3]) + bytes([0x00])*40 + bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3]) + bytes([0x00])*40
    payload = bytearray(f)
    print('teste3')
            

    eop = bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3])
    eopReplaced = bytes([0x00]) + bytes([0xf1]) +  bytes([0x00]) + bytes([0xf2]) +  bytes([0x00]) + bytes([0xf3])
    
    payload = payload.replace(eop, eopReplaced)

    emptyHead = bytes([0x00]) * 6
    imgSize = len(payload).to_bytes(4,"big")
    head = imgSize + emptyHead
    
    package = head + payload + eop
    



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

    if response == bytes([0xa1]):
        print("ERRO: EOP não encontrado")
    if response == bytes([0xa2]):
       print("ERRO: EOP está no lugar errado")
    if response == bytes([0xa3]):
        print("Sucesso")
   
    end = time.time()
        

    delta = end - start
    ThroughPut = len(payload)/delta
    OverHead = len(package)/len(payload)

    print("Tempo:      {} s".format(delta))
    print("ThroughPut: {} b/s".format(ThroughPut))
    print("OverHead:   {} %".format(OverHead))
    
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    client()