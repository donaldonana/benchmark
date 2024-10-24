import os
import subprocess
import time
import signal

IPV4 = "130.190.116.99"
SCHEMA = "S9"
VIDEO = "daenerys.mp4"
DURATION = 32
PROCESS = 10

RESULT_FILE = "result/result.txt"
ENERGY_DIR = f"result/energy/{SCHEMA}"
ENERGY_FILE = f"{ENERGY_DIR}/{VIDEO}.txt"

os.makedirs(ENERGY_DIR, exist_ok=True)
 
for i in range(1, 2):
    energy_process = subprocess.Popen(["cpu-energy-meter", "-r"], stdout=open(ENERGY_FILE, 'a'))
    try:
        whiskprocess = subprocess.Popen(["python3", 
                                         f"python/{SCHEMA}.py", 
                                         IPV4, str(PROCESS), 
                                         str(DURATION), 
                                         SCHEMA, 
                                         VIDEO, 
                                         str(i)], 
                                         stdout=open(RESULT_FILE, 'a'))

    finally:
        whiskprocess.wait()
        os.kill(energy_process.pid, signal.SIGINT)

    print(f"{i}")

    time.sleep(3)

print("All actions have been invoked.")
