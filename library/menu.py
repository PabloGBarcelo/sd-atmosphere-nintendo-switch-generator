####################################################################################################
#                                                                                                  #
#  Copyright 2021 - Free license                                                                   #
#  Date: 17/07/21                                                                                  #
#  Url: github.com/pablogbarcelo                                                                   #
#  Detail: Small script to generate atmosphere/hekate files for MicroSD automatically              #
#                                                                                                  #
####################################################################################################

from library.screen import screenClear

#################
# 1 HEKATE      #
# 2 ATMOSPHERE  #
#################

def copyright():
    print('''
############################################################
#  Script autodescargable 0.1 - Nintendo Switch by NeoSX   #
############################################################
''')
    return

def selectPayload():
    selectedSystem = None
    while selectedSystem not in ["1","2","q","Q"]:
        copyright()
        print('''
+---------------------------------------------+
| ¿Qué sistema de carga quieres usar?         |
+---------------------------------------------+
| 1 - HEKATE sobre ATMOSPHERE (recomendado)   |
| 2 - SOLO ATMOSPHERE                         |
+---------------------------------------------+''')
        if selectedSystem != None:
            print('''|   << La opción que escogiste no existe >>   |
+---------------------------------------------+
''')
        selectedSystem = input("q para salir - Introduce el número y pulsa intro: ")
        if selectedSystem not in ["1","2","q","Q"]:
            screenClear()
        
    return selectedSystem
