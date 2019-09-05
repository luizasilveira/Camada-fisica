def payload():

    with open("image.png", "rb") as image:
        payload = image.read()
        payloadSize = bytes(str(len(payload)), "UTF-8")

    return payloadSize

def eopReplaced():

    eop = bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3])
    eopReplaced = bytes([0x00]) + bytes([0xf1]) +  bytes([0x00]) + bytes([0xf2]) +  bytes([0x00]) + bytes([0xf3])
    payloadReplaced =  payload.replace(eop, eopReplaced)

    return payloadReplaced

def allpayloads():
     eachPayload = [eopReplaced()[x:x+128] for x in range(0, len(eopReplaced()), 128)]
     return eachPayload


def mensagem1():
    
    payload = bytes([0x00])
    eopReplaced()
    totalPackage = len(allpayloads()).to_bytes(3,"little")
    # numberPackage = 0
    # emptyHead =  bytes([0x00]) * 3
    messageNumber = bytes([0x01])
    for payloadS in allpayloads():
        payloadSize = len(payloadS).to_bytes(1,"little")

    head = messageNumber + totalPackage + payloadSize
    return head

print(mensagem1())
