import subprocess
import time
import os 
import sys
import signal

def def_handler(sig,frame):
    #Imprimimos "saliendo" en la pantalla
    print("\n\n [!] Saliendo.... \n")
    #Salimos con un codigo de error 1 (erroneo)
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

def command_run(cmd):
    proc = subprocess.run(cmd,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc

def test(proc):
    command_run("sleep 1")
    print(proc.returncode)
    print(proc)
    print(proc.stdout)
    print(proc.stderr)



if __name__ == "__main__":
    hola_como_estas = command_run("sleep 1")
    test(hola_como_estas)
