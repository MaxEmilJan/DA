import smbus

# Jetson Nano i2c Bus 0 (SDA Pin 27, SCL Pin 28)
bus = smbus.SMBus(0)
# address (same as in the arduino script)
address = 0x40

def writeNumber(value):
    # write input value on bus
    bus.write_byte(address, value)
    return -1

def readNumber():
    # get returned value
    number = bus.read_byte(address)
    return number

while True:
    print("Modus eingeben:\n(0 = Aus, 1 = warmes Licht, 2 = kaltes Licht, q = beenden)")
    var = input("")
    if not var:
        continue
    if var == "q":
        quit()
    else:
        pass

    writeNumber(int(var))
    number = readNumber()
    if number == 0:
        print("Aus")
    elif number == 1:
        print("An (warm)")
    elif number == 2:
        print("An (kalt)")
    else:
        print("ungültige Eingabe")

