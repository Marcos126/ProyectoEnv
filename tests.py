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


def npm_install():

    npm_path = Path("/opt/") / "node.tar.xz"
    command_run(f"sudo wget -O {npm_path} https://nodejs.org/dist/v20.14.0/node-v20.14.0-linux-x64.tar.xz")
    command_run(f"sudo tar -vxf {npm_path}")
    command_run(f"sudo rm {npm_path}")


if __name__ == "__main__":
    npm_install()
