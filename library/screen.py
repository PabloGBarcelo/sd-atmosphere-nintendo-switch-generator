####################################################################################################
#                                                                                                  #
#  Copyright 2021 - Free license                                                                   #
#  Date: 17/07/21                                                                                  #
#  Url: github.com/pablogbarcelo                                                                   #
#  Detail: Small script to generate atmosphere/hekate files for MicroSD automatically              #
#                                                                                                  #
####################################################################################################

import os
def screenClear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')
   # print out some text