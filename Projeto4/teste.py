def payload():

    with open("image.png", "rb") as image:
        payload = image.read()
        payloadSize = bytes(str(len(payload)), "UTF-8")

    return payload

def eopReplaced():

    emptyPayload = bytes([0x00])*5

    eop = bytes([0xf1]) + bytes([0xf2]) + bytes([0xf3])
    eopReplaced = bytes([0x00]) + bytes([0xf1]) +  bytes([0x00]) + bytes([0xf2]) +  bytes([0x00]) + bytes([0xf3])

    emptyPayloadReplaced =  emptyPayload.replace(eop, eopReplaced)
    payloadReplaced = payload().replace(eop, eopReplaced)

    return emptyPayloadReplaced, payloadReplaced

def allpayloads():
     eachPayload = [eopReplaced()[0][x:x+128] for x in range(0, len(eopReplaced()), 128)]
     eachPayloadimg = [eopReplaced()[1][x:x+128] for x in range(0, len(eopReplaced()), 128)]

     return eachPayload, eachPayloadimg


def mensagem1():
    
    totalPackage = len(allpayloads()[0]).to_bytes(3,"little")
    # numberPackage = 0
    # emptyHead =  bytes([0x00]) * 3
    messageNumber = bytes([0x01])
    for payloadS in allpayloads()[0]:
        payloadSize = len(payloadS).to_bytes(1,"little")
        print(payloadSize)

    head = messageNumber + totalPackage + payloadSize
    return head

print(eopReplaced()[0])
print(mensagem1())
