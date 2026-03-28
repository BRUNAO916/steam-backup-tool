# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
from datetime import datetime
from colorama import Fore, init
from tkinter import Tk, filedialog

init(autoreset=True)

# =============================
# CONFIG
# =============================

USER_PATH = os.path.expanduser("~")
DESTINO = os.path.join(USER_PATH, "Downloads")
NOME_ARQUIVO = "Steam-Tools_Backup"

# =============================
# VISUAL
# =============================

def linha():
    print(Fore.CYAN + "=" * 50)

def titulo(txt):
    linha()
    print(Fore.YELLOW + f"   {txt}")
    linha()

# =============================
# SELETOR
# =============================

def selecionar_pasta():
    root = Tk()
    root.withdraw()
    return filedialog.askdirectory(initialdir=DESTINO)

# =============================
# STEAM
# =============================

def fechar_steam():
    os.system("taskkill /f /im steam.exe >nul 2>&1")

def abrir_steam(caminho):
    exe = os.path.join(caminho, "steam.exe")
    if os.path.exists(exe):
        subprocess.Popen(exe)

def procurar_steam():
    base = r"C:\Program Files (x86)\Steam"
    return base if os.path.exists(base) else None

def escolher_pasta():
    while True:
        caminho = input("Digite o caminho da Steam: ").strip().strip('"')
        if os.path.exists(caminho):
            return caminho

# =============================
# BACKUP (CORRETO)
# =============================

def copiar_pasta(origem, destino):
    if os.path.exists(origem):
        shutil.copytree(origem, destino, dirs_exist_ok=True)

def fazer_backup(base):
    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    temp = os.path.join(DESTINO, f"temp_{data}")

    titulo("BACKUP")

    os.makedirs(temp)

    # saves + configs
    copiar_pasta(os.path.join(base, "userdata"), os.path.join(temp, "userdata"))
    copiar_pasta(os.path.join(base, "config"), os.path.join(temp, "config"))
    copiar_pasta(os.path.join(base, "appcache"), os.path.join(temp, "appcache"))

    # biblioteca leve (para LuaTools)
    steamapps = os.path.join(base, "steamapps")
    dest_steamapps = os.path.join(temp, "steamapps")

    if os.path.exists(steamapps):
        os.makedirs(dest_steamapps, exist_ok=True)

        for arq in os.listdir(steamapps):
            if arq.endswith(".acf"):
                shutil.copy2(
                    os.path.join(steamapps, arq),
                    os.path.join(dest_steamapps, arq)
                )

    # compactar
    caminho = os.path.join(DESTINO, f"{NOME_ARQUIVO}_{data}")
    shutil.make_archive(caminho, 'zip', temp)
    os.rename(caminho + ".zip", caminho + ".rar")

    shutil.rmtree(temp)

    print(Fore.GREEN + f"\nBackup salvo em:\n{caminho}.rar")

# =============================
# IMPORTAÇÃO (PERFEITA)
# =============================

def copiar_conteudo(origem, destino):
    if not os.path.exists(origem):
        return

    if not os.path.exists(destino):
        os.makedirs(destino)

    for item in os.listdir(origem):
        src = os.path.join(origem, item)
        dst = os.path.join(destino, item)

        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        except:
            pass  # ignora erros pequenos

def importar_backup():
    titulo("IMPORTAR BACKUP")

    origem = selecionar_pasta()

    if not origem:
        print("Nenhuma pasta selecionada.")
        return

    if "userdata" not in os.listdir(origem):
        print("Backup inválido!")
        return

    destino = procurar_steam()
    if not destino:
        destino = escolher_pasta()

    fechar_steam()

    titulo("IMPORTANDO...")

    # saves
    copiar_conteudo(
        os.path.join(origem, "userdata"),
        os.path.join(destino, "userdata")
    )

    # config
    copiar_conteudo(
        os.path.join(origem, "config"),
        os.path.join(destino, "config")
    )

    # cache
    copiar_conteudo(
        os.path.join(origem, "appcache"),
        os.path.join(destino, "appcache")
    )

    # biblioteca (LuaTools)
    origem_steamapps = os.path.join(origem, "steamapps")
    destino_steamapps = os.path.join(destino, "steamapps")

    if os.path.exists(origem_steamapps):
        os.makedirs(destino_steamapps, exist_ok=True)

        for arq in os.listdir(origem_steamapps):
            if arq.endswith(".acf"):
                try:
                    shutil.copy2(
                        os.path.join(origem_steamapps, arq),
                        os.path.join(destino_steamapps, arq)
                    )
                except:
                    pass

        print(Fore.GREEN + "[OK] Biblioteca restaurada")

    abrir_steam(destino)

    titulo("FINALIZADO")
    print(Fore.GREEN + "Importação concluída!")

# =============================
# MENU
# =============================

def menu():
    titulo("STEAM TOOLS BACKUP")

    print("1 - Backup automático")
    print("2 - Backup manual")
    print("3 - Importar backup")

    return input("\nEscolha: ")

# =============================
# MAIN
# =============================

def main():
    while True:
        os.system("cls")
        op = menu()

        if op == "1":
            base = procurar_steam()
            if base:
                fazer_backup(base)

        elif op == "2":
            base = escolher_pasta()
            fazer_backup(base)

        elif op == "3":
            importar_backup()

        else:
            print("Opção inválida!")

        input("\nENTER para continuar...")

if __name__ == "__main__":
    main()