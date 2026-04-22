# -*- coding: utf-8 -*-

import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("=====================================")
    print("Execute o run.bat como administrador!")
    print("=====================================")
    input()
    sys.exit()

import os
import shutil
import subprocess
import string
from datetime import datetime
from colorama import Fore, init
from tkinter import Tk, filedialog

init(autoreset=True)

USER = os.path.expanduser("~")
DESTINO = os.path.join(USER, "Downloads")

# =============================
# VISUAL
# =============================

def titulo(txt):
    print(Fore.CYAN + "\n" + "="*50)
    print(Fore.YELLOW + f"   {txt}")
    print(Fore.CYAN + "="*50)

# =============================
# PROGRESSO
# =============================

def barra(atual, total):
    if total == 0:
        return
    p = min(100, int((atual / total) * 100))
    b = ("#" * (p // 2)).ljust(50)
    print(f"\r[{b}] {p}% ", end="")

def contar(pasta):
    total = 0
    for _, _, files in os.walk(pasta):
        total += len(files)
    return total

def copiar_prog(origem, destino):
    if not os.path.exists(origem):
        return

    total = contar(origem)
    atual = 0

    for raiz, _, files in os.walk(origem):
        rel = os.path.relpath(raiz, origem)
        dest = os.path.join(destino, rel)

        os.makedirs(dest, exist_ok=True)

        for f in files:

            if f.endswith((".log", ".tmp")):
                continue

            try:
                shutil.copy2(os.path.join(raiz, f),
                             os.path.join(dest, f))
            except:
                pass

            atual += 1
            barra(atual, total)

    print()

# =============================
# COMPACTAÇÃO
# =============================

def compactar_backup(pasta):
    print("\nDeseja compactar o backup?")
    print("1 - Sim (.zip)")
    print("2 - Não")

    escolha = input("> ")

    if escolha == "1":
        print("\nCompactando...")

        zip_path = shutil.make_archive(pasta, 'zip', pasta)

        try:
            shutil.rmtree(pasta)
            return zip_path
        except:
            print("Erro ao remover pasta original.")
            return zip_path

    return pasta

# =============================
# STEAM
# =============================

def procurar_steam():
    encontrados = []

    for letra in string.ascii_uppercase:
        drive = f"{letra}:\\"

        if not os.path.exists(drive):
            continue

        caminhos = [
            os.path.join(drive, "Program Files (x86)", "Steam"),
            os.path.join(drive, "Program Files", "Steam")
        ]

        for caminho in caminhos:
            if os.path.exists(caminho):
                encontrados.append(caminho)

    if not encontrados:
        return None

    if len(encontrados) == 1:
        return encontrados[0]

    print("\nInstalações da Steam encontradas:\n")

    for i, c in enumerate(encontrados, 1):
        print(f"{i} - {c}")

    escolha = input("\nEscolha a Steam: ")

    try:
        idx = int(escolha)
        if 1 <= idx <= len(encontrados):
            return encontrados[idx - 1]
    except:
        pass

    print("Escolha inválida, usando a primeira.")
    return encontrados[0]

def fechar_steam():
    print("\nFechando Steam...")
    os.system("taskkill /f /im steam.exe >nul 2>&1")

def abrir_steam(caminho):
    exe = os.path.join(caminho, "steam.exe")

    if os.path.exists(exe):
        print("\nAbrindo Steam...")
        subprocess.Popen(exe)
    else:
        print("steam.exe não encontrado!")

def escolher_pasta():
    while True:
        print("\nDigite o caminho da Steam (ou ENTER para cancelar):")
        p = input("> ").strip().strip('"')

        if not p:
            return None

        if os.path.exists(p):
            return p

        print("Caminho inválido!")

# =============================
# CONTAS
# =============================

def escolher_usuario(userdata_path):
    if not os.path.exists(userdata_path):
        return None

    contas = [d for d in os.listdir(userdata_path)
              if os.path.isdir(os.path.join(userdata_path, d)) and d.isdigit()]

    if not contas:
        return None

    if len(contas) == 1:
        return contas[0]

    print("\nContas encontradas:\n")
    for i, c in enumerate(contas, 1):
        print(f"{i} - {c}")

    print("0 - TODAS")

    escolha = input("\nEscolha: ")

    try:
        idx = int(escolha)

        if idx == 0:
            return "ALL"

        if 1 <= idx <= len(contas):
            return contas[idx - 1]
    except:
        pass

    print("Escolha inválida, usando primeira conta.")
    return contas[0]

# =============================
# BACKUP
# =============================

def fazer_backup(base):
    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    destino_final = os.path.join(DESTINO, f"SteamVault_Backup_{data}")
    os.makedirs(destino_final, exist_ok=True)

    titulo("BACKUP STEAM (LIMPO)")

    userdata = os.path.join(base, "userdata")
    destino_userdata = os.path.join(destino_final, "userdata")

    escolha = escolher_usuario(userdata)

    if escolha == "ALL":
        print("\nCopiando todas as contas...")
        copiar_prog(userdata, destino_userdata)

    elif escolha:
        print(f"\nCopiando conta {escolha}...")
        copiar_prog(
            os.path.join(userdata, escolha),
            os.path.join(destino_userdata, escolha)
        )
    else:
        print("Nenhuma conta encontrada.")

    print("\nCopiando config/stplug-in...")
    src = os.path.join(base, "config", "stplug-in")

    if os.path.exists(src):
        copiar_prog(src, os.path.join(destino_final, "config", "stplug-in"))
    else:
        print("stplug-in não encontrado.")

    print("\nCopiando appcache/stats...")
    src = os.path.join(base, "appcache", "stats")

    if os.path.exists(src):
        copiar_prog(src, os.path.join(destino_final, "appcache", "stats"))
    else:
        print("stats não encontrado.")

    resultado = compactar_backup(destino_final)

    print(Fore.GREEN + "\n" + "="*50)
    print(Fore.GREEN + "   BACKUP FINALIZADO")
    print(Fore.GREEN + "="*50)
    print(Fore.GREEN + f"\nLocal do backup:\n{resultado}")

# =============================
# IMPORTAR
# =============================

def copiar_conteudo(origem, destino):
    if not os.path.exists(origem):
        return

    for item in os.listdir(origem):
        src = os.path.join(origem, item)
        dst = os.path.join(destino, item)

        if os.path.isdir(src):
            copiar_prog(src, dst)
        else:
            shutil.copy2(src, dst)

def importar():
    titulo("IMPORTAR")

    root = Tk()
    root.withdraw()
    origem = filedialog.askdirectory()

    if not origem:
        print("Nenhuma pasta selecionada.")
        return

    steam = procurar_steam()

    if not steam:
        steam = escolher_pasta()

    if not steam:
        print("Nenhuma Steam selecionada!")
        return

    fechar_steam()

    copiar_conteudo(os.path.join(origem, "userdata"),
                    os.path.join(steam, "userdata"))

    copiar_conteudo(os.path.join(origem, "config", "stplug-in"),
                    os.path.join(steam, "config", "stplug-in"))

    copiar_conteudo(os.path.join(origem, "appcache", "stats"),
                    os.path.join(steam, "appcache", "stats"))

    abrir_steam(steam)

    titulo("FINALIZADO")
    print("Restaurado com sucesso!")

# =============================
# MENU
# =============================

def menu():
    titulo("STEAM VAULT BACKUP")
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
            steam = procurar_steam()
            if steam:
                fazer_backup(steam)
            else:
                print("Steam não encontrada!")

        elif op == "2":
            pasta = escolher_pasta()
            if pasta:
                fazer_backup(pasta)

        elif op == "3":
            importar()

        else:
            print("Opção inválida!")

        input("\nENTER...")

if __name__ == "__main__":
    main()
