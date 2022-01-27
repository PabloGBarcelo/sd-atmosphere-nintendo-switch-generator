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
from dotenv import main
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
    print("Limpiando archivos...")
    test = os.listdir(".")
    for item in test:
        if item.endswith(".zip"):
            os.remove(os.path.join(".", item))
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
                    os.rename(os.getcwd()+"/"+item, os.getcwd()+"/switch/"+item)
                else:
                    # for windows platfrom
                    os.rename(os.getcwd()+"\\"+item, os.getcwd()+"\\switch\\"+item)
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
kip1patch=nosigchk
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
        os.rename(os.getcwd()+"/caffeine.nsp", os.getcwd()+"/pegascape/caffeine.nsp")
        if selectedSystem == "1":
            os.rename(os.getcwd()+"/bootlogo.bmp", os.getcwd()+"/bootloader/bootlogo.bmp")
            os.rename(os.getcwd()+"/hekate_ipl.ini", os.getcwd()+"/bootloader/hekate_ipl.ini")
            binFiles = os.listdir(".")
            for item in binFiles:
                if item.endswith(".bin"):
                    shutil.copy2(os.getcwd()+"/"+item,os.getcwd()+"/atmosphere/reboot_payload.bin")
                    os.rename(os.getcwd()+"/"+item, os.getcwd()+"/Payload Hekate para tegraRCM/payload.bin")
    else:
        # for windows platfrom
        os.rename(os.getcwd()+"\\caffeine.nsp", os.getcwd()+"\\pegascape\\caffeine.nsp")
        if selectedSystem == "1":
            os.rename(os.getcwd()+"\\bootlogo.bmp", os.getcwd()+"\\bootloader\\bootlogo.bmp")
            os.rename(os.getcwd()+"\\hekate_ipl.ini", os.getcwd()+"\\bootloader\\hekate_ipl.ini")
            binFiles = os.listdir(".")
            for item in binFiles:
                if item.endswith(".bin"):
                    shutil.copy2(os.getcwd()+"\\"+item,os.getcwd()+"\\atmosphere\\reboot_payload.bin")
                    os.rename(os.getcwd()+"\\"+item, os.getcwd()+"\\Payload Hekate para tegraRCM\\payload.bin")
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
                data = requests.get(value['url'])
                if data.status_code == 200:
                    if value['source'] == 'github':
                        data = pq(data.text)
                        #mainData = pq(data('.release-main-section'))
                        mainData = pq(data('div[data-test-selector="release-card"]'))
                        title = pq(mainData('.Link--primary')[0])
                        print("Versión detectada: {0}".format(title.text()))
                        # if key == 'sigpatches' and optionSelected == "1":
                        #     fileToDownload = 1 # Second position in sigpatches for hekate in iTotalJustice
                        # else:
                        # fileToDownload = 0 # Fisrt file for rest of them
                        fileName = pq(mainData('.Box-row')[value['position']])
                        urlFile = pq(mainData('.Box-row')[value['position']])('a')
                        print("Descargando {0}".format(fileName.text()))
                        file = requests.get(baseUrl+urlFile.attr('href'), allow_redirects=True)
                        if file.status_code == 200:
                            fileName = pq(fileName('.text-bold')).text()
                            open(fileName, 'wb').write(file.content)
                            print("Descarga completa\n")
                            if key in files.keys():
                                files[key] = fileName
                    else:
                        print("Descargando {0}".format(key))
                        open("bootlogo.bmp", 'wb').write(data.content)
                        print("Descarga completa\n")

                else:
                    print("Ha habido un error intentando descargar Atmosphere\n")
                    return False
            except:
                return False
    return True