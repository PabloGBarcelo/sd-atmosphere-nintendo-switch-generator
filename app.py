####################################################################################################
#                                                                                                  #
#  Copyright 2021 - Free license                                                                   #
#  Date: 17/07/21                                                                                  #
#  Url: github.com/pablogbarcelo                                                                   #
#  Detail: Small script to generate atmosphere/hekate files for MicroSD automatically              #
#                                                                                                  #
####################################################################################################

from library.files_manager import extractFiles, deleteZips, createExtraFolders, changeDirectory, moveNRO, createHekateIPL, adaptFiles, firstClean, downloadFiles
from library.menu import selectPayload

sdFolder = "microSD"

langSystem = {
    "1": "HEKATE SOBRE ATMOSPHERE",
    "2": "SOLO ATMOSPHERE",
    "Q": "SALIR",
    "q": "SALIR"
}

files = {
    'atmosphere' : None,
    'hekate' : None,
    'sigpatches' : None
}

def main():
    selectedSystem = selectPayload()
    checkTest = []
    if selectedSystem in ["1","2"]:
        firstClean(sdFolder)
        createExtraFolders(sdFolder)
        changeDirectory(sdFolder)
        checkTest.append(downloadFiles(selectedSystem, files))
        if False not in checkTest:
            extractFiles(files)
            deleteZips()
            moveNRO()
            createExtraFolders("pegascape")
            if selectedSystem == "1":
                createExtraFolders("Payload Hekate para tegraRCM")
                createHekateIPL()
            adaptFiles(selectedSystem)
            print("\nNeoSX, EOLiano desde 2002.\nTienes la carpeta microsd ya lista en este mismo directorio, cópia el contenido a tu tarjeta microSD y a disfrutar.")
            input("Presiona ENTER para finalizar...")
        else:
            firstClean(sdFolder)
            print("Se ha encontrado un error durante el proceso, OPERACION CANCELADA.")
            input("Presiona ENTER para finalizar...")
    return

main()
