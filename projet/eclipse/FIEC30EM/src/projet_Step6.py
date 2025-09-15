import serial;
from serial.serialutil import SerialException
import time
import matplotlib.pyplot as plt

serialPort = serial.Serial();
serialPort.baudrate = 1000000;
serialPort.port = 'COM3'; #'/dev/cu.usbmodem34B7DA617AC42'
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
    serialPort.flush();
    startTime = time.time()
    endTime = startTime
    lines = []
    while(endTime - startTime < 10):
        endTime = time.time()        
        line = serialPort.readline()
        # line = line.rstrip()
        lines.append(line)
    cmd = "s";
    serialPort.write(cmd.encode(encoding="ascii"))
    serialPort.flush();
    serialPort.close()        
    print('Port closed')
    times = [];
    values = [];
    for row in lines:        
        temp = row.decode('ascii').split(":")
        times.append(float(int(temp[0])/1000000.0))
        values.append(temp[1])
    print(len(times));
    print(times[len(times)-1]);
    print(len(values));
    print(values[len(values)-1]);
    plt.plot(times, values)
    plt.show()    
    # Écriture dans un fichier texte csv
    file = open("data.txt", "w")
    file.write("time (s), value\n")
    for row in lines:
        row = row.rstrip() # remove CR/LF
        file.write(row.decode('ascii') + "\n")
    file.close()    
except Exception as exception :    
    print('Exception occurred while writing/reading characters')
    print(exception)
    serialPort.close()
    print('Port closed')
