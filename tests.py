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
    proc = subprocess.run(cmd
                          ,shell=True
                          ,stdin=subprocess.PIPE
                          ,stdout=subprocess.PIPE
                          ,stderr=subprocess.PIPE
                          ,text=True)
    if  proc.returncode == 0:
        print(f"[+] {cmd} Ejecutado correctemente")
    else: 
        print(f"[!] Error ejecutando\n\n\n {cmd}\n\n\n")
        print(proc.stdout)
        print(proc.stderr)
        sys.exit(1)
    return proc



def npmInstall():
    installPath = Path("/opt/")
    file = Path("/opt/") / "node.tar.xz"
    url = "https://nodejs.org/dist/v20.14.0/node-v20.14.0-linux-x64.tar.xz"
    wgetInstall(url,file,installPath)

def goInstall():
    installPath = Path("/opt/")
    file = Path("/opt/") / "go.tar.gz"
    url = "https://dl.google.com/go/go1.22.4.linux-amd64.tar.gz"
    wgetInstall(url,file,installPath)

def wgetInstall(url,file,installPath):
    command_run(f"sudo wget -O {installPath} {url} ")
    command_run(f"sudo tar -vxf {file} -C {installPath}")
    command_run(f"sudo rm {file}")

if __name__ == "__main__":
    goInstall()
    npmInstall()
