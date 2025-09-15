import serial;
from serial.serialutil import SerialException
import time
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

def forceStopFunction():
    forceStop.set(True)
    print("Force stop : " + str(forceStop.get()))

def chooseDestionationFolder():
    destionationfolder = filedialog.askdirectory()
    destinationFolderValue.set(destionationfolder)
    print(destionationfolder)

def runTrials():    
    nbTrials = int(nbTrialsSpinbox.get())
    for currentTrial in range(nbTrials):
        
        print("Force stop : " + str(forceStop.get()))
        
        if(forceStop.get() == True):
            stateValue.set("N.A.")
            currentTrialValue.set("1")
            forceStop.set(False)
            break
            
        print("Starting Trial number " + str(currentTrial+1))
        
        stateValue.set("Running")
        currentTrialValue.set(str(currentTrial + 1))
        runButton.config(state=tk.DISABLED)
        browseButton.config(state=tk.DISABLED)
        nbTrialsSpinbox.config(state=tk.DISABLED)
        dataFilesPrefixValueEntry.config(state=tk.DISABLED)
        destinationFolderValueEntry.config(state=tk.DISABLED)
        
        app.update()
        
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
            while(endTime - startTime < 2):
                endTime = time.time()        
                line = serialPort.readline()
                # line = line.rstrip()
                lines.append(line)
            cmd = "s";
            stateValue.set("Pending")
            serialPort.write(cmd.encode(encoding="ascii"))
            serialPort.flush();
            serialPort.close()        
            print('Serial port closed')
            times = [];
            values = [];
            for row in lines:        
                temp = row.decode('ascii').split(":")
                times.append(float(int(temp[0])/1000000.0))
                values.append(float(temp[1]))
            #print(len(times));
            #print(times[len(times)-1]);
            #print(len(values));
            #print(values[len(values)-1]);
            print('Waiting for plot to be closed...')
            plt.plot(times, values)
            plt.show()    
            # Écriture dans un fichier texte csv
            print('Save data to csv file')
            fileName = dataFilesPrefixValue.get() + "data_" + str(currentTrial+1) + ".txt"
            destination = os.path.join(destinationFolderValue.get(), fileName)
            print(destination)
            file = open(destination, "w")
            file.write("time (µs), value\n")
            for row in lines:
                row = row.rstrip() # remove CR/LF
                rowValue = row.decode('ISO-8859-1').replace(":", ",")
                file.write(rowValue + "\n")
            file.close()   
            print("Trial number " + str(currentTrial+1) + " ended") 
        except Exception as exception :    
            print('Exception occurred while writing/reading characters')
            print(exception)
            serialPort.close()
            print('Port closed')
        
        print('Exit function')
        runButton.config(state=tk.NORMAL)
        browseButton.config(state=tk.NORMAL)
        nbTrialsSpinbox.config(state=tk.NORMAL)
        dataFilesPrefixValueEntry.config(state=tk.NORMAL)
        destinationFolderValueEntry.config(state=tk.NORMAL)
        
# Main prog
app = tk.Tk()
app.title("Gestionnaire d'essais")

frame1 = ttk.Frame(app)
frame1.pack(fill=tk.BOTH)
frame1.grid_rowconfigure(0, weight=1)
frame1.grid_rowconfigure(1, weight=1)
frame1.grid_rowconfigure(2, weight=1)
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_columnconfigure(1, weight=1)
frame1.grid_columnconfigure(2, weight=1)

destinationFolderValue = tk.StringVar()
dataFilesPrefixValue = tk.StringVar()

nbTrialsLabel = ttk.Label(frame1,  text="Number of trials : ")
nbTrialsLabel.grid(row = 0, column = 0, sticky = "w", padx = 0, pady = 0);
nbTrialsSpinbox = ttk.Spinbox(frame1, from_=1, to=10)
nbTrialsSpinbox.set(1)
nbTrialsSpinbox.grid(row = 0, column = 1, sticky="we", padx = 0, pady = 0, columnspan = 2);

dataFilesPrefixLabel = ttk.Label(frame1,  text="Data files prefix : ")
dataFilesPrefixLabel.grid(row = 1, column = 0, sticky = "w", padx = 0, pady = 0);
dataFilesPrefixValueEntry = ttk.Entry(frame1)
dataFilesPrefixValueEntry.insert(0, "FSR_")
dataFilesPrefixValueEntry.grid(row = 1, column = 1, sticky = "we", padx = 0, pady = 0, columnspan = 2);

destinationFolderLabel = ttk.Label(frame1,  text="Destination folder : ")
destinationFolderLabel.grid(row = 2, column = 0, sticky = "w", padx = 0, pady = 0);

destinationFolderValueEntry = ttk.Entry(frame1, textvariable=destinationFolderValue)
destinationFolderValueEntry.grid(row = 2, column = 1, sticky = "we", padx = 0, pady = 0);
browseButton = ttk.Button(frame1, text = "Browse...", command = chooseDestionationFolder);
browseButton.grid(row = 2, column = 2, sticky="we", padx = 0, pady = 0);

separator = ttk.Separator(app,orient='horizontal')
separator.pack(fill='x')

frame2 = ttk.Frame(app)
frame2.pack(fill=tk.BOTH)
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_columnconfigure(1, weight=1)
frame2.grid_columnconfigure(2, weight=1)
frame2.grid_columnconfigure(3, weight=1)
frame2.grid_columnconfigure(4, weight=1)

stateValue = tk.StringVar()
currentTrialValue = tk.StringVar()
forceStop = tk.BooleanVar()
forceStop.set(False)

currentTrialLabel = ttk.Label(frame2,  text="Current trial : ")
currentTrialLabel.grid(row = 0, column = 0, sticky = "e", padx = 0, pady = 0);
currentTrialValueLabel = ttk.Label(frame2,  textvariable = currentTrialValue)
currentTrialValueLabel.grid(row = 0, column = 1, sticky = "e", padx = 0, pady = 0);
stateValueLabel = ttk.Label(frame2, textvariable = stateValue)
stateValueLabel.grid(row = 0, column = 2, sticky = "e", padx = 0, pady = 0);
runButton = ttk.Button(frame2, text = "Run", command = runTrials); # !!! runTrials without ()
runButton.grid(row = 0, column = 3, sticky="e", padx = 0, pady = 0);
stopButton = ttk.Button(frame2, text = "Stop", command = forceStopFunction)
stopButton.grid(row = 0, column = 4, sticky="e", padx = 0, pady = 0);
    
stateValue.set("N.A.")
currentTrialValue.set("1") 
dataFilesPrefixValue.set("FSR_")

app.geometry("400x165")
app.resizable(True,False)
app.mainloop()
