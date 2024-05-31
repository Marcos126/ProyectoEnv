import subprocess
import re
from tqdm import tqdm

def install_packages(packages):
    for package in packages:
        with subprocess.Popen(['sudo', 'apt-get', 'install', '-y', package],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, bufsize=1) as proc, tqdm(desc=package) as bar:
            for line in proc.stdout:
                if "Desempaquetando" in line:
                    bar.update(25)  # Ajustar según la estimación de progreso por salida
                elif "Configurando" in line:
                    bar.update(75)  # Ajustar según la estimación de progreso por salida
                print(line, end='')

packages = ["curl", "vim"]
install_packages(packages)

