import subprocess
import sys
import signal

def def_handler(sig,frame):
    print("\n\n [!] Saliendo ....")

    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

def responder():
    response = subprocess.run(["ping","-w","1","0.0.0.1"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    contador = 0
    while response.returncode !=0:
        response = subprocess.run(["ping","-w","1","0.0.0.1"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print(response.returncode , contador)
        contador += 1
    print(response.returncode)

if __name__ == '__main__': 
    responder()

