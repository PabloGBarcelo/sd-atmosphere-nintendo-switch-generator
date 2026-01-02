####################################################################################################
#                                                                                                  #
#  Copyright 2021 - Free license                                                                   #
#  Date: 17/07/21                                                                                  #
#  Url: github.com/pablogbarcelo                                                                   #
#  Detail: Small script to generate atmosphere/hekate files for MicroSD automatically              #
#                                                                                                  #
####################################################################################################

import os
import shutil
import requests
from zipfile import ZipFile
from pyquery import PyQuery as pq
import requests
import json
baseUrl = "https://github.com/"
urls_github = json.load(open('./assets/files.json'))


def extractFiles(files):
    print("Descomprimiendo archivos...")
    for file in files:
        if files[file] != None and '.zip' in files[file]:
            with ZipFile(files[file], 'r') as zipObj:
                # Extract all the contents of zip file in current directory
                zipObj.extractall()
    return


def deleteZips():
    print("Limpiando archivos zip...")
    # Limpiar zips del directorio actual (microSD)
    test = os.listdir(".")
    for item in test:
        if item.endswith(".zip"):
            os.remove(os.path.join(".", item))
    
    # Limpiar zips del directorio raíz
    if os.name == "posix":
        root_dir = os.path.dirname(os.getcwd())
    else:
        root_dir = os.path.dirname(os.getcwd())
    
    root_files = os.listdir(root_dir)
    for item in root_files:
        if item.endswith(".zip"):
            zip_path = os.path.join(root_dir, item)
            try:
                os.remove(zip_path)
                print(f"Eliminado: {item}")
            except Exception as e:
                print(f"No se pudo eliminar {item}: {e}")
    return


def createExtraFolders(name):
    print("Creando carpeta {0}".format(name))
    os.makedirs("{0}".format(name))
    return


def changeDirectory(sdFolder):
    # for mac and linux(here, os.name is 'posix')
    print("Cambiando a ruta principal de carpeta "+sdFolder)
    if os.name == "posix":
        os.chdir(os.getcwd()+"/"+sdFolder)
    else:
        # for windows platfrom
        os.chdir(os.getcwd()+"\\"+sdFolder)
    return


def moveNRO():
    apps = os.listdir(".")
    for item in apps:
        if item.endswith(".nro"):
            if 'hbmenu' not in item:
                if os.name == "posix":
                    os.rename(os.getcwd()+"/"+item,
                              os.getcwd()+"/switch/"+item)
                else:
                    # for windows platfrom
                    os.rename(os.getcwd()+"\\"+item,
                              os.getcwd()+"\\switch\\"+item)
    return


def createHekateIPL():
    print("Creando Hekate IPL")
    with open("hekate_ipl.ini", 'w') as newFile:
        newFile.write('''[config]
autoboot=0
autoboot_list=0
bootwait=0
autohosoff=0
autonogc=1
updater2p=1
backlight=100

[CFW - sysMMC]
fss0=atmosphere/package3
kip1patch=nosigchk
atmosphere=1
emummc_force_disable=1
icon=bootloader/res/icon_payload.bmp

[CFW - emuMMC]
fss0=atmosphere/package3
emummcforce=1
atmosphere=1
icon=bootloader/res/icon_payload.bmp
logopath=bootloader/bootlogo.bmp

[Stock - sysMMC]
fss0=atmosphere/package3
emummc_force_disable=1
stock=1
icon=bootloader/res/icon_switch.bmp
''')
    print("Creación de Hekate IPL con éxito")
    return


def adaptFiles(selectedSystem):
    print("Finalizando operaciones...")
    if os.name == "posix":
        if os.path.exists(os.getcwd()+"/caffeine.nsp"):
            os.rename(os.getcwd()+"/caffeine.nsp",
                      os.getcwd()+"/pegascape/caffeine.nsp")
        
        if selectedSystem == "1":
            if os.path.exists(os.getcwd()+"/bootlogo.bmp") and os.path.exists(os.getcwd()+"/bootloader"):
                os.rename(os.getcwd()+"/bootlogo.bmp",
                          os.getcwd()+"/bootloader/bootlogo.bmp")
            
            if os.path.exists(os.getcwd()+"/hekate_ipl.ini") and os.path.exists(os.getcwd()+"/bootloader"):
                os.rename(os.getcwd()+"/hekate_ipl.ini",
                          os.getcwd()+"/bootloader/hekate_ipl.ini")
            
            binFiles = os.listdir(".")
            for item in binFiles:
                if item.endswith(".bin"):
                    if os.path.exists(os.getcwd()+"/atmosphere"):
                        shutil.copy2(os.getcwd()+"/"+item, os.getcwd() +
                                     "/atmosphere/reboot_payload.bin")
                    os.rename(os.getcwd()+"/"+item, os.getcwd() +
                              "/Payload Hekate para tegraRCM/payload.bin")
    else:
        if os.path.exists(os.getcwd()+"\\caffeine.nsp"):
            os.rename(os.getcwd()+"\\caffeine.nsp",
                      os.getcwd()+"\\pegascape\\caffeine.nsp")
        
        if selectedSystem == "1":
            if os.path.exists(os.getcwd()+"\\bootlogo.bmp") and os.path.exists(os.getcwd()+"\\bootloader"):
                os.rename(os.getcwd()+"\\bootlogo.bmp",
                          os.getcwd()+"\\bootloader\\bootlogo.bmp")
            
            if os.path.exists(os.getcwd()+"\\hekate_ipl.ini") and os.path.exists(os.getcwd()+"\\bootloader"):
                os.rename(os.getcwd()+"\\hekate_ipl.ini",
                          os.getcwd()+"\\bootloader\\hekate_ipl.ini")
            
            binFiles = os.listdir(".")
            for item in binFiles:
                if item.endswith(".bin"):
                    if os.path.exists(os.getcwd()+"\\atmosphere"):
                        shutil.copy2(os.getcwd()+"\\"+item, os.getcwd() +
                                     "\\atmosphere\\reboot_payload.bin")
                    os.rename(os.getcwd()+"\\"+item, os.getcwd() +
                              "\\Payload Hekate para tegraRCM\\payload.bin")
    print("¡PROCESO FINALIZADO CON ÉXITO!")
    return


def firstClean(sdFolder):
    if os.path.exists(sdFolder):
        print("Limpiando archivos...")
        shutil.rmtree(sdFolder)
        print("Limpieza completada")
    return


def downloadFiles(optionSelected, files):
    for key, value in urls_github.items():
        if optionSelected in value['option']:
            try:
                print(value['url'])
                if value['source'] == 'github':
                    api_url = value['url'].replace('https://github.com/', 'https://api.github.com/repos/').replace('/releases', '/releases/latest')
                    
                    data = requests.get(api_url)
                    if data.status_code == 200:
                        release_data = data.json()
                        version = release_data.get('tag_name', release_data.get('name', 'Desconocida'))
                        print("Versión detectada: {0}".format(version))
                        assets = release_data.get('assets', [])
                        if len(assets) > value['position']:
                            asset = assets[value['position']]
                            fileName = asset['name']
                            downloadUrl = asset['browser_download_url']
                            
                            print("Descargando {0}".format(fileName))
                            file = requests.get(downloadUrl, allow_redirects=True)
                            if file.status_code == 200:
                                open(fileName, 'wb').write(file.content)
                                print("Descarga completa\n")
                                if key in files.keys():
                                    files[key] = fileName
                            else:
                                print("Error al descargar el archivo {0}\n".format(fileName))
                                return False
                        else:
                            print("No se encontró el archivo en la posición {0}\n".format(value['position']))
                            return False
                    else:
                        print("Ha habido un error intentando acceder a {0}\n".format(key))
                        return False
                elif value['source'] == 'google':
                    if key == "bootlogo":
                        data = requests.get(value['url'])
                        if data.status_code == 200:
                            print("Descargando {0}".format(key))
                            open("bootlogo.bmp", 'wb').write(data.content)
                            print("Descarga completa\n")
                        else:
                            print("Error al descargar {0}\n".format(key))
                            return False
            except Exception as e:
                print("Error: {0}".format(str(e)))
                return False
    return True
