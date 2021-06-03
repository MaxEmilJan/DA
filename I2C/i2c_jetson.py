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
    print("Modus eingeben (0 = Aus, 1 = An):")
    var = input("")
    if not var:
        continue

    writeNumber(int(var))
    number = readNumber()
    if number == 0:
        print("Aus")
    elif number == 1:
        print("An")
    else:
        print("ungültige Eingabe")