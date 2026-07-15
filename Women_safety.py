from machine import UART, Pin
import time

# Setup UART for SIM800L
uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Sound sensor digital pin
sound_sensor = Pin(15, Pin.IN)

def send_cmd(cmd, delay=1):
    uart1.write(cmd + '\r\n')
    time.sleep(delay)
    response = b''
    while uart1.any():
        try:
            response += uart1.read()
        except:
            pass
    print(response.decode('utf-8', 'ignore'))

def send_sms():
    send_cmd('AT', 1)
    send_cmd('AT+CMGF=1', 1)
    send_cmd('AT+CSCS="GSM"', 1)
    send_cmd('AT+CMGS="+919987611345"', 2)  # Replace with your number
    uart1.write('HELP NEEDED!!\nLocation:\nLatitude:19.046028\nLongitude:72.870766\x1A')  # Ctrl+Z
    time.sleep(5)
    print("SMS Sent.")

# Allow SIM800L to initialize
time.sleep(5)

print("Monitoring sound...")

while True:
    if sound_sensor.value() == 1:  # Sound detected
        print("Sound detected!")
        send_sms()
        time.sleep(10)  # Wait before allowing another SMS
