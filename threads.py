import threading 
import time
import subprocess



def command_run(cmd):
    proc = subprocess.run(cmd, shell=True,text=True,stdout=True,stderr=True,stdin=True)
    if proc.returncode == 0:
        print(f"{cmd} Finalizo con exito")
    else: 
        print(f"\n\n\nError al ejecutar\n\n\n {cmd}\n\n\n")


def task():
    print("Iniciando Task")
    time.sleep(1)
    print("Task finalizada")

def tosk():
    print("Iniciando Tosk")
    time.sleep(2)
    print("Tosk finalizada")

def tusk():
    print("Iniciando Tusk")
    time.sleep(3)
    print("Tusk finalizada")

funciones = [tusk,task,tosk]

threads = []
    
start_time = time.perf_counter()

for funcion in funciones:
    thread = threading.Thread(target=funcion)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end_time = time.perf_counter()

print(f"Esto tardo {end_time - start_time: 0.2f}")
