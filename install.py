import threading
import subprocess 
import os
import signal
import sys
from pathlib import Path
from pwn import log


#------------------------------------------CRTL + C-----------------------------------------------

#Esta funcion es para capturar el crtl + c.
def def_handler(sig,frame):
    #Imprimimos "saliendo" en la pantalla
    print("\n\n [!] Saliendo.... \n")
    #Salimos con un codigo de error 1 (erroneo)
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

#------------------------------------------Globals-----------------------------------------------


home_path = os.environ.get('HOME')

def reading():
    with open("Packages.txt",'r') as file:
        packages = [line.strip() for line in file if line.strip()]
    return packages
package_list = reading()



#------------------------------------------SINCRONOS-----------------------------------------------

def command_run(cmd):
    proc = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # if not proc.returncode == 0:
    #     print(f"[+] {cmd} Ejecutado correctemente")
    # else: 
        # print(f"[!] Error ejecutando\n\n\n {cmd}\n\n\n")
        # sys.exit(1)
    return proc


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

    if len(packages_to_install) == 0:
        p2 = log.progress("Paquetes")
        p2.success("No hay paquetes por instalar")
    else:
        p2 = log.progress(f"{len(packages_to_install)} : Paquetes por instalar")
        counter = 0 
        install_errors = []
        for install in packages_to_install: 
            counter += 1
            p2.status(f"{install}")
            installe_package = command_run(f"sudo apt-get install -y {install}")
            if installe_package.returncode !=0:
                install_errors.append(install)
            if len(install_errors) != 0:
                print(f"Hubieron errores en la instalacion de {len(install_errors)} paquetes")
            else:
                print("---------------------------------------------")
                print(f"[+] {install} Instalado correctamente [+]")
            if counter == len(packages_to_install):
                print("---------------------------------------------")
                p2.success("Paquetes instalados correctemnte")
        for error in install_errors:
            log.info(f"[!] Error instalando{error}")

#------------------------------------------ASINCRONOS-----------------------------------------------

#En esta funcion se instala una nerd font que es la que yo utilizo.
def nerd_fonts():
    p4 = log.progress("Nerd Fonts")
    
    #Url de la fuente
    p4.status("Seteando la variable de la fuente")
    font_url = "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/Hack.zip"
    #Carpeta destino
    p4.status("Seteando la variable del destino")
    font_destination = Path("/usr/share/fonts/hack")
    #Revisamos que exista y sino existe la creamos
    p4.status("Verificando la existencia de la ruta de instalacion")
    if not font_destination.exists():
        command_run(f"sudo mkdir -p {font_destination}")
    #Este va a ser el nombre de el archivo que vamos a descargar
    p4.status("Seteando el path de la descarga")
    hack_font_file = Path(font_destination) / "hack.zip"
    #Lo descargamos
    p4.status("Descargando el archivos")
    command_run(f"sudo wget -O {hack_font_file} {font_url}")
    #Lo extraemos
    p4.status("Descomprimiendo el archivo")
    command_run(f"sudo 7z e {hack_font_file} -o{font_destination} -y")
    #Lo borramos
    p4.status("Eliminando el archivo")
    command_run(f"sudo rm {hack_font_file}")
    p4.success("Hack Nerd Font Instalada correctamente ")

#En esta funcion se instala kitty, haciendo uso de el kitty bundle
    
def kitty_install():
    p5 = log.progress("Kitty Install")
    
    #URL del bundle
    p5.status("Seteando la variable de la descarga")
    kitty_url = "https://github.com/kovidgoyal/kitty/releases/download/v0.35.1/kitty-0.35.1-x86_64.txz"
    
    # Destino de la instalacion
    p5.status("Seteando la variable de destino")
    kitty_destination = Path("/opt/kitty")
    
    #Creacion y verificacion de la carpeta /opt/kitty
    p5.status("Verificando que el path exista")
    if not kitty_destination.exists():
        command_run(f"sudo mkdir {kitty_destination}")
    
    #Seteando el destino
    p5.status("Seteando el destino de la descarga")
    tar_file = Path(kitty_destination) / "kitty.txz"
    
    #Descargar el archivo kitty.txz a el destino
    p5.status("Descargando el archivo")
    command_run(f"sudo wget {kitty_url} -O {tar_file}")
    
    #Lo extraemos
    p5.status("Descomprimiendo el archivo")
    command_run(f"sudo tar -vxf {tar_file} -C {kitty_destination}")
    
    
    #Lo borramos
    p5.status("Borrando el archivo")
    command_run(f"sudo rm {tar_file}")
    
    p5.success("Kitty Instalado Correctamente")


#En esta funcion voy a traer unos archivos de configuracion de mi repositorio de github y los voy a instalar en los .config correspondientes

def tryconfig():
    p6 = log.progress("Config Repos")
    
    #Paquetes a instalar la configuracion
    repo_packages = ["nvim","kitty","picom","polybar" , "sxhkd", "bspwm"]
    #Seteando la url del repositorio
    url_config_repo = "https://github.com/Marcos126/tryconfig"   
    
    #Seteando la carpeta en la que van a ser instalados posteriormente
    p6.status("Seteando el path de destino")
    configs = Path(f"{home_path}/.config")
    
    #Seteando el destino de el git clone
    p6.status("Seteando el path de descarga")
    destination_repo = Path("/tmp/tryconfig")
    p6.status("Descargando el repositorio")
    
    if destination_repo.exists():
        command_run(f"rm -rf {destination_repo}")
        command_run(f"git clone {url_config_repo} {destination_repo}")
    else:
        command_run(f"git clone {url_config_repo} {destination_repo}")

    #Verificar que la carpeta exista
    p6.status("Verificando que la carpeta de .config exista")
    if not configs.exists():
        command_run(f"mkdir {configs}")

    #Moviendo las carpetas a .config
    p6.status("Moviendo los paquetes a sus carpetas")
    counter = 0
    
    for package in repo_packages:
        pool_configs = Path(destination_repo) / package
        configs_destiny = Path(configs) / package
        p6.status(f"Moviendo {package} a su destino")
        command_run(f"rm -rf {configs_destiny}")
        command_run(f"mv {pool_configs} {configs_destiny}")
        counter += 1
        if counter == len(repo_packages):
            p6.status("Archivos de configuracion instalados")
    #Copiando Pictures del repo en el home del usuario
    p6.status("Copiando Pictures")

    pic = Path(f"{home_path}/Pictures")
    if not pic.exists():
        pic.mkdir()

    command_run(f"mv -f {destination_repo}/Pictures/* {home_path}/Pictures ")
    #Copiando el .zshrc del repo
    p6.status("copiando .zshrc")
    command_run(f"mv {destination_repo}/.zshrc {home_path}/.zshrc")
    #Copiando el .p10k del repo
    p6.status("Copiando .p10k")
    command_run(f"mv {destination_repo}/.p10k.zsh {home_path}/.p10k.zsh")

    target = Path(f"{home_path}/.config/bin")
    if not target.exists:
        target.mkdir()
        command_run(f"touch {target}/target")
    p6.success("Config de Github instalada correctamente")



#Instlacion de lsd
    
def lsd_install():
    p7 = log.progress("LSD Install")
    

    # URL de la descarga
    p7.status("Seteando la url de lsd")
    lsd_url = "https://github.com/lsd-rs/lsd/releases/download/v1.1.2/lsd-musl_1.1.2_amd64.deb"
    
    # Path de la descarga
    p7.status("Seteando el path de descarga")
    lsd_destination = Path("/tmp/lsd/")
    
    #Nombre del archivo
    p7.status("Seteando el nombre del archivo")
    deb_file = Path(lsd_destination) / "lsd.deb" 
    
    # Verificar que el path de la descarga exista
    p7.status("Verificando que exista el path de descarga")
    if not lsd_destination.exists():
        command_run(f"mkdir {lsd_destination}")
    
    #Descargar el archivo
    p7.status("Descargando el archivo")
    command_run(f"wget {lsd_url} -O {deb_file}")
    
    #Instalar el archivo
    p7.status("Instalando el LSD")
    command_run(f"sudo apt-get install -y {deb_file}")
    
    #Borrar el archivo
    p7.status("Borrando el archivo de instalacion")
    command_run(f"rm -rf {lsd_destination}")

    p7.success("LSD instalado correctamente")

#Instalacion de la ultima version de nvim

def nvim_install():
    p8 = log.progress("Nvim Install")
    
    #URL del bundle
    p8.status("Seteando la URL")
    nvim_url = "https://github.com/neovim/neovim/releases/download/v0.10.0/nvim-linux64.tar.gz"
    # Destino de la instalacion
    p8.status("Seteando el destino")
    nvim_destination = Path("/opt/")
    #Creacion y verificacion de la carpeta /opt/
    p8.status("Verificando que exista la carpeta")
    if not nvim_destination.exists():
        command_run(f"sudo mkdir {nvim_destination}")
    #Seteando el destino
    p8.status("Seteando el nombre de la descarga ")
    tar_file = Path(nvim_destination) / "nvim.tar.gz"
    #Descargar el archivo
    p8.status("Descargando el archivo")
    command_run(f"sudo wget {nvim_url} -O {tar_file}")
    #Extraer el contenido
    p8.status("Descomprimiendo el archivo")
    command_run(f"sudo tar -vxf {tar_file} -C {nvim_destination}")
    # Borrar el archivo
    p8.status("Borrando el archivo")
    command_run(f"sudo rm {tar_file}")
    p8.success("Nvim Instalado correctamente")

#Instalacion de NodeJS 

#Instalacion de golang

#Instalacion de oh my zsh

def zsh_install():
    p9 = log.progress("ZSH Install")
    
    #URL de descarga
    p9.status("Seteando el url de ohmyzsh")
    oh_my_zsh = "curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
    
    #Verificando la carpeta de instalacion
    p9.status("Verificando ~/.oh-my-zsh")
    install_path = Path(f"{home_path}/.oh-my-zsh")
    
    #Condicional para borrar la carpeta en caso de que este
    if install_path.exists():

        #Borrando la carpeta
        p9.status("Borrando ~/.oh-my-zsh ")
        command_run(f"rm -rf {install_path}")

    #Instalando oh my zsh
    command_run(f"{oh_my_zsh} | bash")
    command_run(f"source {home_path}/.zshrc")
    command_run(f"git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git {home_path}/.oh-my-zsh/custom/themes/powerlevel10k")
    p9.success("Oh-My-ZSH Instalado correctamente")


#Cambio de la shell
def change_shell():

    p10 = log.progress("Changing Shell")
    
    #Cambiando de shell
    result_userName=subprocess.run(["whoami"], capture_output=True, text=True)
    userName = result_userName.stdout.strip()
    p10.status("Cambiando de shell")
    proc = command_run(f"sudo chsh -s /bin/zsh {userName}")
    if proc.returncode == 0:
        p10.success("Shell cambiada")
    else:
        p10.failure("Error al cambiar la shell")




if __name__ == '__main__':

    proc = command_run("sudo apt-get update")
    if proc.returncode == 0:

        p1 = log.progress("Instalando dependencias")

        package_checker()
        functions = [nerd_fonts, kitty_install, lsd_install, nvim_install, zsh_install, change_shell]
        threads = []
        
        for function in functions:
            thread = threading.Thread(target=function)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        tryconfig()
        print(" INSTALACION FINALIZADA CON EXITO ")
        p1.success("Instalacion finalizada con exito")

        sys.exit(0)
    else:
        print("Error al dar permisos de sudo")
        sys.exit(1)

