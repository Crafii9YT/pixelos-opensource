# Before you edit this code please note I coded this not very well
# I know I coded shit. I warned you
# And please dont copy the code. You can make your own PixelOS from this but say at least its based on PixelOS

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

SERVER_ADDONS_URL = "http://peach.fps.ms:11231/addons"
SERVER_KEYS_URL = "http://peach.fps.ms:11231/keys/keys.php"
url = "http://peach.fps.ms:11231/pixelos-code/PixelOS_Custom.py"
SERVER_ADDONS_INDEXURL = "index.php"
BENUTZERNAME_FILE = "Systemdateien/Setup/benutzername.txt"
PASSWORD_FILE = "Systemdateien/Setup/password.txt"

directoryzwei = "Systemdateien"
directory = os.path.join(directoryzwei, "Textdokumente")
directorydrei = os.path.join(directoryzwei, "Add-Ons")
directoryvier = os.path.join(directoryzwei, "Setup")
app_installer_dir = os.path.join(directoryzwei, "App Installer Files")
keys_dir = os.path.join(directoryzwei, "Keys")
command_dir = os.path.join(directoryzwei, "Commands")
pqu_dir = os.path.join(directoryzwei, "PixelOS_Code")
script_path = os.path.join(pqu_dir, "PixelOS_Custom.py")

ziel_datei = pqu_dir + "\PixelOS_Custom.py"


BETA_MODE = False
OPEN_BETA_MODE = True
VERSION = "CUSTOM_1"

if OPEN_BETA_MODE:
    SERVER_VERSION_URL = "http://peach.fps.ms:11231/version/version_beta.php"
elif OPEN_BETA_MODE == False:
    SERVER_VERSION_URL = "http://peach.fps.ms:11231/version/version_release.php"

def find_pios_key_file():
    for filename in os.listdir(keys_dir):
        if filename.endswith(".pios"):
            return os.path.join(keys_dir, filename)
    return None

def get_valid_keys_from_server():
    """Lädt gültige Keys von der angegebenen Server-URL."""
    try:
        with urllib.request.urlopen(SERVER_KEYS_URL) as response:
            html = response.read().decode("utf-8")

            keys = re.findall(r'[A-Za-z0-9\-\_\)\(ß]+', html)
            return keys
    except Exception as e:
        print(f"Fehler beim Abrufen der Keys vom Server: {e}")
        return []

def validate_local_key():
    """Überprüft, ob der lokale Key in der Serverliste steht."""
    key_file_path = find_pios_key_file()
    if key_file_path is None:
        print("❌ Keine .pios-Keydatei gefunden in Systemdateien/Keys/")
        input("Drücke Enter zum Beenden...")
        exit(1)

    with open(key_file_path, "r", encoding="utf-8") as file:
        key_content = file.read().strip()

    valid_keys = get_valid_keys_from_server()

    if key_content in valid_keys:
        print(" ")
    else:
        print("❌ Ungültiger Key oder nicht auf dem Server registriert.")
        input("Drücke Enter zum Beenden...")
        exit(1)

if BETA_MODE:
    validate_local_key()

def load_addon(addon_path):
    spec = importlib.util.spec_from_file_location("addon_module", addon_path)
    addon_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(addon_module)
    return addon_module

def list_server_addons():
    try:
        with urllib.request.urlopen(SERVER_ADDONS_URL + "/" + SERVER_ADDONS_INDEXURL) as response:
            html = response.read().decode("utf-8")
            addons = re.findall(r'href="([^"]+\.py)"', html)
            addons = sorted(list(set(addons)))
            return addons
    except Exception as e:
        print(f"Fehler beim Abrufen der Add-Ons vom Server: {e}")
        return []

def install_pios_file(file_path):
    import zipfile
    import shutil
    try:
        print(f"Entpacke {file_path} ...")
        extract_dir = os.path.join(app_installer_dir, "entpackt")
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print("Datei entpackt.")

        install_dir = os.path.join(extract_dir, "install")
        if os.path.exists(install_dir):
            install_script = os.path.join(install_dir, "install.py")
            if os.path.exists(install_script):
                print("Starte Installationsskript...")
                spec = importlib.util.spec_from_file_location("install_module", install_script)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "main"):
                    module.main()
                print("Installation abgeschlossen.")
            else:
                print("Kein install.py gefunden.")
        else:
            print("Kein 'install'-Ordner in der entpackten Datei gefunden.")
    except Exception as e:
        print(f"Fehler bei der Installation: {e}")

def get_server_version():
    """Lädt die Version von der Server-URL."""
    try:
        with urllib.request.urlopen(SERVER_VERSION_URL) as response:
            version = response.read().decode("utf-8").strip()
            return version
    except Exception as e:
        print(f"Fehler beim Abrufen der Server-Version: {e}")
        return None

def check_for_update(local_version):
    server_version = get_server_version()
    if not server_version:
        return False, None

    return server_version != local_version, server_version

def set_terminal_color():

    print("=== Terminalfarbe ändern ===")
    system = platform.system()
    if system == "Windows":
        windows_colors = {
            '0': 'Schwarz', '1': 'Blau', '2': 'Grün', '3': 'Cyan',
            '4': 'Rot', '5': 'Magenta', '6': 'Gelb', '7': 'Weiß',
            '8': 'Grau', '9': 'Hellblau', 'A': 'Hellgrün', 'B': 'Hellcyan',
            'C': 'Hellrot', 'D': 'Hellmagenta', 'E': 'Hellgelb', 'F': 'Hellweiß'
        }
        for k, v in windows_colors.items():
            print(f"{k} = {v}")
        code = input("Hintergrund+Vordergrund (z.B. 0A für schwarz Hintergrund + hellgrün Text) > ").strip().upper()
        if re.match(r'^[0-9A-F]{2}$', code):
            try:
                os.system(f"color {code}")
                print("Farbe gesetzt.")
            except Exception as e:
                print(f"Fehler beim Setzen der Farbe: {e}")
        else:
            print("Ungültiger Code. Zwei Hex-Ziffern erwartet.")
    else:
        ansi = {
            'schwarz': 30, 'rot': 31, 'gruen': 32, 'gelb': 33,
            'blau': 34, 'magenta': 35, 'cyan': 36, 'weiss': 37
        }
        print("Verfügbare Farben: " + ", ".join(ansi.keys()))
        fg = input("Textfarbe (z.B. rot) > ").strip().lower()
        bg = input("Hintergrundfarbe (z.B. schwarz) > ").strip().lower()
        if fg in ansi and bg in ansi:
            print(f"\033[{ansi[fg]}m\033[{ansi[bg] + 10}m", end="")
            print("Farbe gesetzt. Um zurückzusetzen: Eingabe '\\033[0m' in deinem Code oder die Sitzung neu starten.")
        else:
            print("Ungültige Farbeingabe.")

def execute_command_file(command_name, args=None):
    """
    Sucht im Ordner `command_dir` nach einer Datei mit dem Namen `command_name` (mit oder ohne .py)
    und führt diese aus. Führt nur Dateien aus, die gültigen Python-Code enthalten.
    Fallback: wenn importlib spec/loader nicht verfügbar ist, wird `runpy.run_path` verwendet.
    Gibt True zurück, wenn eine passende Python-Datei gefunden und ausgeführt wurde, sonst False.
    """
    if args is None:
        args = []

    candidates = [
        os.path.join(command_dir, command_name),
        os.path.join(command_dir, f"{command_name}.py")
    ]

    for candidate in candidates:
        if os.path.isfile(candidate):
            try:
                with open(candidate, "r", encoding="utf-8") as f:
                    source = f.read()
                compile(source, candidate, "exec")
            except Exception:
                continue

            prev_argv = sys.argv[:]
            sys.argv = [candidate] + args
            module = None
            module_name = f"command_{os.path.basename(candidate)}_{int(time.time()*1000)}"
            try:
                spec = importlib.util.spec_from_file_location(module_name, candidate)
                if spec is not None and getattr(spec, "loader", None) is not None:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                else:
                    runpy.run_path(candidate, run_name=module_name)
                if module is not None and hasattr(module, "main"):
                    try:
                        module.main()
                    except TypeError:
                        module.main()
                sys.argv = prev_argv
                return True
            except Exception as e:
                sys.argv = prev_argv
                print(f"Error: '{candidate}': {e}")
                return True
    return False


if os.path.exists(BENUTZERNAME_FILE):
    with open(BENUTZERNAME_FILE, "r", encoding="utf-8") as file:
        benutzername = file.read().strip()
else:
    benutzername = ""

if os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, "r", encoding="utf-8") as file:
        password = file.read().strip()

if not benutzername:
    print("\033[H\033[J", end="")
    print("-------- PixelOS Setup --------")
    print("Mit der Nutzung dieses Programms stimmst du den Nutzungsbedingungen zu. http://peach.fps.ms:11231")
    input("Druecke Enter um fortzufahren")
    print("\033[H\033[J", end="")
    print("-------- PixelOS Setup --------")
    while True:
        ter = input("root@pixelos > ")
        if ter == "createdir":
            directoryzwei = "Systemdateien"
            if not os.path.exists(directoryzwei):
                os.makedirs(directoryzwei)
            dir_input = input()
            test = os.path.join(directoryzwei, dir_input)
            if not os.path.exists(test):
                os.makedirs(test)
        elif ter == "username":
            benutzername = input()
            with open(BENUTZERNAME_FILE, "w", encoding="utf-8") as file:
                file.write(benutzername)
        elif ter == "password":
            password = input()
            with open(PASSWORD_FILE, "w", encoding="utf-8") as file:
                file.write(password)
        elif ter == "color":
            set_terminal_color()
        elif ter == "clear":
            print("\033[H\033[J", end="")
            print("-------- PixelOS Setup --------")
        elif ter == "help":
            print("Eingebaute Befehle:")
            print("color - Terminalfarbe ändern")
            print("createdir - Erstellt die notwendigen Ordner")
            print("username - Ändert/setzt den Benutzernamen")
            print("clear - Cleart das Terminal")
            print("checkupdate - Überprüft auf verfügbare Updates")
            print("exit - Beendet das Terminal")
        elif ter == "exit":
            break
        else:
            parts = ter.split()
            cmd = parts[0]
            args = parts[1:]
            handled = execute_command_file(cmd, args)
            if not handled:
                print("Unknown command.")

while True:
    ter_pref = benutzername + "@pixelos > "
    print("\033[H\033[J", end="")
    print("-------- PixelOS --------")
    print("Hallo " + benutzername)
    print("Gebe eine Zahl von 1 bis 6 ein")
    print("1 = Taschenrechner")
    print("2 = Texteditor")
    print("3 = Add-Ons")
    print("4 = Terminal")
    print("5 = Version")
    print("6 = Mitwirkende")
    print("7 = Beenden")
    eing_eins = int(input("> "))
    if eing_eins == 1:
        print("Willkommen beim Taschenrechner. Willst du plus, minus, mal oder geteilt:")
        print("1 = Plus")
        print("2 = Minus")
        print("3 = Mal")
        print("4 = Geteilt")
        eing_zwei = int(input())
        print("Gebe deine erste Zahl ein")
        eing_drei = int(input())
        print("Jetzt die Zweite")
        eing_vier = int(input())
        if eing_zwei == 1:
            print("Ergebnis:")
            print(eing_drei + eing_vier)
        elif eing_zwei == 2:
            print("Ergebniss:")
            print(eing_drei - eing_vier)
        elif eing_zwei == 3:
            print("Ergebniss:")
            print(eing_drei * eing_vier)
        elif eing_zwei == 4:
            if eing_vier == 0:
                print("Du kannst nicht durch 0 teilen!!!")
            else:
                print("Ergebniss:")
                print(eing_drei / eing_vier)
        else:
            print("Bitte geb eine gueltige Zahl ein!!!")
        input("Druecke enter um fortzufahren")
    elif eing_eins == 2:
        print("Texteditor Optionen:")
        print("1 = Neue Datei erstellen")
        print("2 = Datei oeffnen")
        print("3 = Datei editieren")
        print("4 = Beenden")
        option = int(input())
        if option == 1:
            print("Geben Sie den Dateinamen ein:")
            filename = input()
            filepath = os.path.join(directory, filename)
            print("Geben Sie den Text ein (beenden mit 'END'):")
            lines = []
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
            with open(filepath, "w", encoding="utf-8") as file:
                file.write("\n".join(lines))
            print(f"Datei {filename} wurde erstellt.")
        elif option == 2:
            print("Geben Sie den Dateinamen ein:")
            filename = input()
            filepath = os.path.join(directory, filename)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as file:
                    print(file.read())
            else:
                print("Datei nicht gefunden.")
        elif option == 3:
            print("Geben Sie den Dateinamen ein:")
            filename = input()
            filepath = os.path.join(directory, filename)
            print("Geben Sie den Text ein (beenden mit 'END'):")
            lines = []
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
            with open(filepath, "w", encoding="utf-8") as file:
                file.write("\n".join(lines))
            print(f"Datei {filename} wurde gespeichert.")
        elif option == 4:
            continue
        else:
            print("Ungueltige Option, bitte versuchen Sie es erneut.")
        input("Druecke enter um fortzufahren")
    elif eing_eins == 3:
        print("Add-Ons Optionen:")
        print("1 = Klassische Add-Ons (vom Server laden / starten)")
        print("2 = App Installer (.pios Dateien installieren)")
        addon_option = int(input())

        if addon_option == 1:
            print("1 = Add-On von Server auswaehlen und herunterladen")
            print("2 = Vorhandene Add-Ons anzeigen und laden")
            sub_option = int(input())

            if sub_option == 1:
                server_addons = list_server_addons()
                py_addons = [a for a in server_addons if a.endswith(".py")]
                if not py_addons:
                    print("Keine Add-Ons gefunden.")
                else:
                    print("Add-Ons auf dem Server:")
                    for i, addon in enumerate(py_addons):
                        print(f"{i + 1} = {os.path.basename(addon)}")
                    auswahl = int(input("Waehle ein Add-On: "))
                    if 1 <= auswahl <= len(py_addons):
                        addon_name = os.path.basename(py_addons[auswahl - 1])
                        url = SERVER_ADDONS_URL + "/" + addon_name
                        save_path = os.path.join(directorydrei, addon_name)
                        urllib.request.urlretrieve(url, save_path)
                        print(f"{addon_name} wurde gespeichert.")
            elif sub_option == 2:
                addons = [f for f in os.listdir(directorydrei) if f.endswith('.py')]
                for i, addon in enumerate(addons):
                    print(f"{i + 1} = {addon}")
                auswahl = int(input("Waehle ein Add-On zum Laden: "))
                if 1 <= auswahl <= len(addons):
                    addon_path = os.path.join(directorydrei, addons[auswahl - 1])
                    addon_module = load_addon(addon_path)
                    if hasattr(addon_module, 'main'):
                        addon_module.main()
            else:
                print("Ungueltige Auswahl.")
            input("Druecke enter um fortzufahren")

        elif addon_option == 2:
            print("App Installer Optionen:")
            print("1 = .pios Datei vom Server herunterladen und installieren")
            print("2 = Lokale .pios Datei installieren")
            sub_option = int(input())

            if sub_option == 1:
                server_addons = list_server_addons()
                pios_files = [a for a in server_addons if a.endswith(".pios")]
                if not pios_files:
                    print("Keine .pios Dateien auf dem Server gefunden.")
                else:
                    print("Verfuegbare .pios Dateien:")
                    for i, addon in enumerate(pios_files):
                        print(f"{i + 1} = {os.path.basename(addon)}")
                    auswahl = int(input("Waehle eine Datei: "))
                    if 1 <= auswahl <= len(pios_files):
                        addon_name = os.path.basename(pios_files[auswahl - 1])
                        url = SERVER_ADDONS_URL + "/" + addon_name
                        save_path = os.path.join(app_installer_dir, addon_name)
                        urllib.request.urlretrieve(url, save_path)
                        print(f"{addon_name} wurde heruntergeladen.")
                        install_pios_file(save_path)
            elif sub_option == 2:
                files = [f for f in os.listdir(app_installer_dir) if f.endswith(".pios")]
                if not files:
                    print("Keine .pios Dateien gefunden.")
                else:
                    for i, f in enumerate(files):
                        print(f"{i + 1} = {f}")
                    auswahl = int(input("Waehle eine Datei: "))
                    if 1 <= auswahl <= len(files):
                        path = os.path.join(app_installer_dir, files[auswahl - 1])
                        install_pios_file(path)
            else:
                print("Ungueltige Auswahl.")

        else:
            print("Ungueltige Option.")
    elif eing_eins == 4:
        print("\033[H\033[J", end="")
        print("-------- PixelOS Terminal --------")
        root = False
        while True:
            ter_os = input(ter_pref)
            if ter_os == "color":
                set_terminal_color()
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
                if root:
                    benutzername = input()
                    with open(BENUTZERNAME_FILE, "w", encoding="utf-8") as file:
                        file.write(benutzername)
                else:
                    print("You need root for this Command")
            elif ter_os == "password":
                if root:
                    password = input()
                    with open(PASSWORD_FILE, "w", encoding="utf-8") as file:
                        file.write(password)
                else:
                    print("You need root for this Command")
            elif ter_os == "checkupdate":
                update_available, server_version = check_for_update(VERSION)
                if update_available:
                    print(f"⚠ Update verfügbar! (Server Version: {server_version}, Deine Version: {VERSION})")
                else:
                    print("✔ PixelOS ist auf dem neuesten Stand.")
            elif ter_os == "help":
                print("Eingebaute Befehle:")
                print("color - Terminalfarbe ändern")
                print("createdir - Erstellt die notwendigen Ordner")
                print("username - Ändert/setzt den Benutzernamen")
                print("clear - Cleart das Terminal")
                print("checkupdate - Überprüft auf verfügbare Updates")
                print("password - Aendert das Passwort")
                print("su - Wechselt zu root")
                print("buildpios - Buildet dein eigenes PixelOS")
                print("downloadpios - Läd den Quellcode herunter")
                print("exit - Beendet das Terminal")
            elif ter_os == "repair":
                directoryzwei = "Systemdateien"
                if not os.path.exists(directoryzwei):
                    os.makedirs(directoryzwei)

                directory = os.path.join(directoryzwei, "Textdokumente")
                if not os.path.exists(directory):
                    os.makedirs(directory)

                directorydrei = os.path.join(directoryzwei, "Add-Ons")
                if not os.path.exists(directorydrei):
                    os.makedirs(directorydrei)

                directoryvier = os.path.join(directoryzwei, "Setup")
                if not os.path.exists(directoryvier):
                    os.makedirs(directoryvier)

                app_installer_dir = os.path.join(directoryzwei, "App Installer Files")
                if not os.path.exists(app_installer_dir):
                    os.makedirs(app_installer_dir)

                keys_dir = os.path.join(directoryzwei, "Keys")
                if not os.path.exists(keys_dir):
                    os.makedirs(keys_dir)

                command_dir = os.path.join(directoryzwei, "Commands")
                if not os.path.exists(command_dir):
                    os.makedirs(command_dir)
                benutzername = "root"
                with open(BENUTZERNAME_FILE, "w", encoding="utf-8") as file:
                    file.write(benutzername)
            elif ter_os == "pixelfetch":
                print("PixelOS")
                print("Version:", VERSION)
                print("Username:", benutzername)
            elif ter_os == "win":
                if platform.system() == "Windows":
                    subprocess.run(["powershell.exe"])
                    print("\033[H\033[J", end="")
                    print("-------- PixelOS Terminal --------")
                else:
                    print("Error performing command: Dieser Befehl ist nur unter Windows verfügbar.") 
            elif ter_os == "su":
                passw = input("Please enter your Password: ")
                if passw == password:
                    ter_pref = "root@pixelos > "
                    root = True
                else:
                    print("Wrong password")
            elif ter_os == "buildpios":
                command = ["pyinstaller", "--onefile", script_path]
                try:
                    subprocess.run(command, check=True)
                    print("Build erfolgreich abgeschlossen!")
                except subprocess.CalledProcessError as e:
                    print("Fehler beim Erstellen:", e)
            elif ter_os == "downloadpios":
                try:
                    urllib.request.urlretrieve(url, ziel_datei)
                    print(f"Download abgeschlossen: {ziel_datei}")
                except Exception as e:
                    print("Fehler beim Download:", e)
            elif ter_os == "exit":
                if ter_pref == "root@pixelos > ":
                    root = False
                    ter_pref = benutzername + "@pixelos > "
                else:
                    break
            else:
                parts = ter_os.split()
                cmd = parts[0]
                args = parts[1:]
                handled = execute_command_file(cmd, args)
                if not handled:
                    print("Unknown command.")
    elif eing_eins == 5:
        print("PixelOS Version " + VERSION + " BETA")
        print("Release Datum: 15.11.25")
        print("Um PixelOS zu aktualisieren, benutze den Updater (PixelOS_Updater.exe)")
        input("Druecke enter um fortzufahren")
    elif eing_eins == 6:
        print("Owner und Dev: Leonard1412")
        print("Owner: Crafii9")
        input("Druecke enter um fortzufahren")
    elif eing_eins == 7:
        wait = input("Druecke Enter um das Programm zu beenden")
        break
    elif eing_eins == 99:
        print("Easter Egg :D")
        input("Druecke enter um fortzufahren")

