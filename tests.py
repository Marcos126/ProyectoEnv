import subprocess
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
    return proc

package_list = ["htop","xclip","apt-utils","feh","sqlmap","vim","nano"]

def package_checker():
    packages_to_install = []
    installed_packages = []
    counter = 0
    for package in package_list:
        check = subprocess.run(f"dpkg -s {package}",shell=True,text=True, stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        counter += 1
        if check.returncode != 0:
            packages_to_install.append(package)
        else: 
            installed_packages.append(package)

    p2 = log.progress(f"{len(packages_to_install)} : Paquetes por instalar")
    counter = 0 
    install_errors = []
    for install in packages_to_install: 
        counter += 1
        p2.status(f"{install}")
        installe_package = command_run(f"sudo apt-get install -y {install}")
        if installe_package.returncode !=0:
            install_errors.append(install)
        else:
            print("-----------------------------")
            print(f"[+] {install} Instalado correctamente [+]")
            print("-----------------------------")
        if counter == len(packages_to_install):
            p2.success("Paquetes instalados correctemnte")

    for error in install_errors:
        log.info(f"[!] Error instalando{error}")



if __name__ == "__main__":
    package_checker()
