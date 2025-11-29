import os
import importlib.util
import runpy
from turtle import clear
import urllib.request
import re
import shutil
import subprocess
import platform
import sys
import time

VERSION = "KERNEL-1.0"

def terminal_open():
            benutzername = "user"
            ter_pref = benutzername + "@pixelos > "
            print("\033[H\033[J", end="")
            print("-------- PixelOS KERNEL --------")
            root = False
            while True:
                ter_os = input(ter_pref)
                if ter_os == "color":
                    print("Only availabe in a compatible Distro")
                elif ter_os == "createdir":
                    if root:
                        directoryzwei = "Systemdateien"
                        if not os.path.exists(directoryzwei):
                            os.makedirs(directoryzwei)
                        dir_input = input()
                        test = os.path.join(directoryzwei, dir_input)
                        if not os.path.exists(test):
                            os.makedirs(test)
                    else:
                        print("You need root for this Command")
                elif ter_os == "clear":
                    print("\033[H\033[J", end="")
                    print("-------- PixelOS Terminal --------")
                elif ter_os == "username":
                    print("Only availabe in an commpatible Distro")
                elif ter_os == "password":
                    print("Only availabe in an commpatible Distro")
                elif ter_os == "checkupdate":
                    print("Only availabe in an commpatible Distro")
                elif ter_os == "help":
                    print("Eingebaute Befehle:")
                    print("color - Terminalfarbe ändern")
                    print("createdir - Erstellt die notwendigen Ordner")
                    print("clear - Cleart das Terminal")
                    print("checkupdate - Überprüft auf verfügbare Updates")
                    print("su - Wechselt zu root")
                    print("exit - Beendet das Terminal")
                elif ter_os == "pixelfetch":
                    print("PixelOS")
                    print("Version:", VERSION)
                    print("Username:", benutzername)
                elif ter_os == "win":
                    if platform.system() == "Windows":
                        subprocess.run(["powershell.exe"])
                        print("\033[H\033[J", end="")
                        print("-------- PixelOS KERNEL --------")
                    else:
                        print("Error performing command: Dieser Befehl ist nur unter Windows verfügbar.") 
                elif ter_os == "su":
                    ter_pref = "root@pixelos > "
                    root = True
                elif ter_os == "exit":
                    if ter_pref == "root@pixelos > ":
                        root = False
                        ter_pref = benutzername + "@pixelos > "
                    else:
                        break
                else:
                    print("Unknown command.")

terminal_open()

