import threading
import subprocess
import os 
import signal
import sys
import time
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

result_userName=subprocess.run(["whoami"], capture_output=True, text=True)
userName = result_userName.stdout.strip()

def reading():
    with open("Packages.txt",'r') as file:
        packages = [line.strip() for line in file if line.strip()]
    return packages

package_list = reading()



#------------------------------------------SINCRONOS-----------------------------------------------

def command_run(command):
    command_signal = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if command_signal.returncode != 0:
        print(f"Ocurrion un error en la ejecucion de {command}")

def check_package(package):
    result = subprocess.run(["dpkg","-s",package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode !=0:
        dpkg_result = subprocess.run(["sudo","DEBIAN_FRONTEND=noninteractive","apt-get","install",package,"-y"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if dpkg_result.returncode != 0:
            print(f"Error al instalar {package}")



#------------------------------------------ASINCRONOS-----------------------------------------------

#En esta funcion se va a instalar brave, el cual es mi navegador favorito.

def brave_install():
    p3.status("Descargando las GPG Keys")
    #Descarga de la llave GPG.
    command_run(["sudo", "curl", "-fsSLo", "/usr/share/keyrings/brave-browser-archive-keyring.gpg", "https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg"])
    
    #Concat de el repositorio de brave al source.list.
    p3.status("Declarando los repositorios APT")
    repo_entry = "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"
    p3.status("Agregando los respositorios APT")
    with open("/etc/apt/sources.list.d/brave-browser-release.list", "w") as file:
        file.write(repo_entry)
#Actualizar los repositorios de apt para ver el paquete de brave.
    p3.status("Actualizando los repositorios APT")
    command_run(["sudo", "apt-get", "update"])

    #Instalar brave.
    p3.status("Instalando Brave-browser con APT")
    response = subprocess.run(["sudo", "apt-get", "install","brave-browser","-y"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    counter = 1 
    while response.returncode !=0: 
        counter += 1
        p3.status(f"Estan habiendo problemas para instalar brave. ReturnCode: {response.returncode} Intentos: {counter}]")
        time.sleep(5)
        response = subprocess.run(["sudo", "apt-get", "install","brave-browser","-y"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p3.success("Brave instalado correctamente")


#En esta funcion se instala una nerd font que es la que yo utilizo.

def nerd_fonts():
    #Url de la fuente
    p4.status("Seteando la variable de la fuente")
    font_url = "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/Hack.zip"
    
    #Carpeta destino
    p4.status("Seteando la variable del destino")
    font_destination = Path("/usr/share/fonts/hack")
    
    #Revisamos que exista y sino existe la creamos
    p4.status("Verificando la existencia de la ruta de instalacion")
    font_destination.mkdir(parents=True,exist_ok=True)
    
    #Este va a ser el nombre de el archivo que vamos a descargar
    p4.status("Seteando el path de la descarga")
    p7z_file = Path(font_destination) / "hack.zip"
    
    #Lo descargamos
    p4.status("Descargando el archivos")
    command_run(["wget","-O",p7z_file,font_url])
    
    #Lo extraemos
    p4.status("Descomprimiendo el archivo")
    command_run(["7z","e",p7z_file, f"-o{font_destination}"])
    
    #Lo borramos
    p4.status("Eliminando el archivo")
    command_run(["rm", p7z_file])
    
    p4.success("Hack Nerd Font Instalada correctamente ")


#En esta funcion se instala kitty, haciendo uso de el kitty bundle
    



def kitty_install():
    #URL del bundle
    p5.status("Seteando la variable de la descarga")
    kitty_url = "https://github.com/kovidgoyal/kitty/releases/download/v0.35.0/kitty-0.35.0-x86_64.txz"
    
    # Destino de la instalacion
    p5.status("Seteando la variable de destino")
    kitty_destination = "/opt/kitty"
    
    #Creacion y verificacion de la carpeta /opt/kitty
    p5.status("Verificando que el path exista")
    Path(kitty_destination).mkdir(parents=True,exist_ok=True)
    
    #Seteando el destino
    p5.status("Seteando el destino de la descarga")
    tar_file = Path(kitty_destination) / "kitty.txz"
    
    #Descargar el archivo kitty.txz a el destino
    p5.status("Descargando el archivo")
    command_run(["wget", "-q",kitty_url,"-O",str(tar_file)])
    
    #Lo extraemos
    p5.status("Descomprimiendo el archivo")
    command_run(["tar","-vxf",str(tar_file), "-C",kitty_destination])
    
    #Lo borramos
    p5.status("Borrando el archivo")
    command_run(["rm", str(tar_file)])
    p5.success("Kitty Instalado Correctamente")


#En esta funcion voy a traer unos archivos de configuracion de mi repositorio de github y los voy a instalar en los .config correspondientes

def tryconfig():

    #Paquetes a instalar la configuracion
    repo_packages = ["nvim","kitty","picom","polybar" , "sxhkd", "bspwm"]
    #Seteando la url del repositorio
    p6.status("Seteando la url del repositorio")
    url_config_repo = "https://github.com/Marcos126/tryconfig"   
    
    #Seteando la carpeta en la que van a ser instalados posteriormente
    p6.status("Seteando el path de destino")
    configs_destiny = Path(f"{home_path}/.config")
    
    #Seteando el destino de el git clone
    p6.status("Seteando el path de descarga")
    destination_repo = Path("/tmp/tryconfig")
    
    #Como esta funcion se va a repetir unas veces y no quiero nuevamente o tire error cuando lo haga, agrego un condicional para que solo haga git clone si la carpeat no existe
    p6.status("Descargando el repositorio")
    command_run(["git","clone",url_config_repo, destination_repo])
    
    #Verificar que la carpeta exista
    p6.status("Verificando que la carpeta de .config exista")
    configs_destiny.mkdir(parents=True, exist_ok=True)
    
    #Moviendo las carpetas a .config
    p6.status("Moviendo los paquetes a sus carpetas")
    counter = 0
    
    for package in repo_packages:
        pool_configs = Path(destination_repo) / package
        configs = Path(configs_destiny) / package
        p6.status(f"Moviendo {package} a su destino")
        command_run(["mv", pool_configs, configs])
        
        counter += 1
        if counter == len(repo_packages):
            p6.success("Config de Github instalada correctamente")

#Instlacion de lsd
    
def lsd_install():

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
    lsd_destination.mkdir(parents=True,exist_ok=True)
    
    #Descargar el archivo
    p7.status("Descargando el archivo")
    command_run(["wget", "-q", lsd_url, "-O", deb_file])
    
    #Instalar el archivo
    p7.status("Instalando el LSD")
    command_run(["sudo","apt-get","install","-y",deb_file])
    
    #Borrar el archivo
    p7.status("Borrando el archivo de instalacion")
    command_run(["rm","-rf", lsd_destination])
    p7.success("LSD instalado correctamente")

#Instalacion de la ultima version de nvim

def nvim_install():

    #URL del bundle
    p8.status("Seteando la URL")
    nvim_url = "https://github.com/neovim/neovim/releases/download/v0.10.0/nvim-linux64.tar.gz"
    # Destino de la instalacion
    p8.status("Seteando el destino")
    nvim_destination = "/opt/"
    #Creacion y verificacion de la carpeta /opt/
    p8.status("Verificando que exista la carpeta")
    Path(nvim_destination).mkdir(parents=True,exist_ok=True)
    #Seteando el destino
    p8.status("Seteando el nombre de la descarga ")
    tar_file = Path(nvim_destination) / "nvim.tar.gz"
    #Descargar el archivo
    p8.status("Descargando el archivo")
    command_run(["wget", "-q",nvim_url,"-O",str(tar_file)])
    #Extraer el contenido
    p8.status("Descomprimiendo el archivo")
    command_run(["tar","-vxf",str(tar_file), "-C",nvim_destination])
    # Borrar el archivo
    p8.status("Borrando el archivo")
    command_run(["rm", str(tar_file)])
    p8.success("Nvim Instalado correctamente")


#Instalacion de oh my zsh

def zsh_install():

    #URL de descarga
    p9.status("Seteando el url de ohmyzsh")
    oh_my_zsh = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
    
    #Ruta del archivo
    p9.status("Seteando el nombre de la descarga")
    ohmy_installer = "/tmp/install.sh"
    
    #Descargando el archivo
    p9.status("Descargando el instalador")
    command_run(["wget","-qO", ohmy_installer, oh_my_zsh])
    
    #Verificando la carpeta de instalacion
    p9.status("Verificando ~/.oh-my-zsh")
    install_path = Path(f"{home_path}/.oh-my-zsh")
    
    #Condicional para borrar la carpeta en caso de que este
    if install_path.exists():
        #Borrando la carpeta
        p9.status("Borrando ~/.oh-my-zsh ")
        command_run(["rm","-rf",install_path])
        

    #Ejecucion del instalador
    p9.status("Ejecutando el instalador")
    command_run(["bash",ohmy_installer,"--unattended"])
    
    #Borrando el instalador
    p9.status("Borrando el instalador")
    command_run(["rm", ohmy_installer])
    p9.success("Oh-My-ZSH Instalado correctamente")

#Actualizacion del PATH

def update_path():

    #Updateando el PATH
    time.sleep(10)
    p0.status("Updating path")
    with open(f"{home_path}/.zshrc",'a') as file:
        data = f"\nexport PATH=$PATH:/opt/nvim-linux64/bin:/opt/kitty/bin"
        file.write(data)
    p0.success("Path updateado")


#Cambio de la shell
def change_shell():
    #Cambiando de shell
    p10.status("Cambiando de shell")
    command_run(["sudo","chsh","-s","/bin/zsh", userName])
    p10.success("Shell cambiada")



if __name__ == '__main__':

    p1 = log.progress("Iniciando instalacion")
    p2 = log.progress("Paquetes")
    p3 = log.progress("Brave Install")
    p4 = log.progress("Nerd Fonts")
    p5 = log.progress("Kitty Install")
    p6 = log.progress("Config Repos")
    p7 = log.progress("LSD Install")
    p8 = log.progress("Nvim Install")
    p9 = log.progress("ZSH Install")
    p0 = log.progress("Update PATH")
    p10 = log.progress("Changing Shell")

    p1.status("Instalando paquetes dependencias")
    counter=0
    for package in package_list:
        check_package(package)
        counter += 1
        p2.status(f"Instalando {package}")
        if counter == len(package_list):
            p2.success("Dependencias Instaladas correctamente")


    functions = [brave_install,nerd_fonts,kitty_install,tryconfig,lsd_install,nvim_install,zsh_install,update_path,change_shell]
    threads = []

    for function in functions:
        thread = threading.Thread(target=function)
        thread.start()
        threads.append(thread)
        
    time.sleep(5)
