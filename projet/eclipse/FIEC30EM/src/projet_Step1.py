import serial;
from serial.serialutil import SerialException

serialPort = serial.Serial();
serialPort.baudrate = 1000000;
serialPort.port = 'COM4';
serialPort.parity = serial.PARITY_NONE;
serialPort.stopbits = serial.STOPBITS_ONE;
serialPort.bytesize = serial.EIGHTBITS;

try :
    serialPort.open();
except SerialException as serialException:
    print(serialException)
    
if(not serialPort.isOpen()):
    print('Serial port not opened')
    exit()

try :
    print('Serial port opened. Write run character.')
    cmd = "r";
    serialPort.write(cmd.encode(encoding="ascii"))
    serialPort.close()    
    print('Port closed')
except Exception as exception :    
    print('Exception occurred while writing run character')
    print(exception)
    serialPort.close()
    print('Port closed')   