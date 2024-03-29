import os
import time
import sys

if len(sys.argv) != 2:
	print("Usage (assuming USB0): python3 copy.py /dev/ttyUSB0")
	quit()

dev = str(sys.argv[1])
t0 = time.time()
files = os.listdir('.')

print("-----------------------------------------------------")
print("Big folders will take a lot of time at 115200 baud rate!")
print("rdflib folder currently takes around 6 - 10 mn.")
print("If  MCU gets stuck then one should copy the rest using ampy or reformat and relaunch this command.")
print("----------------------------------------------------")

for file in list(files):
	
   cmd = "ampy --port %s --baud 115200 put %s"%(dev,file)
   print(cmd)
   ret = os.system(cmd)
   t1 = time.time()
   print("Time taken till now {} secs.".format(abs(t1-t0)))
