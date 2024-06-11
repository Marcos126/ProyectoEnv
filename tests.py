import subprocess
from pathlib import Path
import sys
from pwn import log
import signal

def def_handler(sig,frame):
    #Imprimimos "saliendo" en la pantalla
    print("\n\n [!] Saliendo.... \n")
    #Salimos con un codigo de error 1 (erroneo)
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

def command_run(cmd):
    proc = subprocess.run(cmd,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if  proc.returncode == 0:
        print(f"[+] {cmd} Ejecutado correctemente")
    else: 
        print(f"[!] Error ejecutando\n\n\n {cmd}\n\n\n")
        print(proc.stdout)
        print(proc.stderr)
        sys.exit(1)
    return proc


def go_install():  

    go_destination = Path("/opt/")
    go_path = Path("/opt/") / "go.tar.gz"
    command_run(f"sudo wget -O {go_path} https://dl.google.com/go/go1.22.4.linux-amd64.tar.gz")
    command_run(f"sudo tar -vxf {go_path} -C {go_destination}")
    command_run(f"sudo rm {go_path}")

if __name__ == "__main__":
    go_install()
