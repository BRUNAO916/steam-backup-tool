# -*- coding: utf-8 -*-

import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def erro_admin():
    print("\n" + "="*45)
    print("ERRO: Execute o run.bat como administrador!")
    print("="*45 + "\n")
    input("Pressione ENTER para sair...")
    sys.exit()

if __name__ == "__main__":
    if not is_admin():
        erro_admin()

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
ESPACO_MINIMO_MB = 500

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
# ESPAÇO EM DISCO
# =============================

def verificar_espaco():
    total, usado, livre = shutil.disk_usage("C:\\")
    livre_mb = livre // (1024 * 1024)

    if livre_mb < ESPACO_MINIMO_MB:
        print(Fore.RED + f"\n[ERRO] Espaço insuficiente no disco C:")
        print(Fore.RED + f"Mínimo necessário: {ESPACO_MINIMO_MB} MB")
        print(Fore.RED + f"Disponível: {livre_mb} MB\n")
        return False

    return True

# =============================
# SELETOR DE PASTA
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
        print("Caminho inválido!")

# =============================
# BACKUP CONFIG
# =============================

def escolher_tipo_backup():
    titulo("TIPO DE BACKUP")

    print("1 - Salvar TUDO")
    print("2 - Biblioteca + saves + conquistas + horas (sem screenshots)")

    escolha = input("\nEscolha: ")

    if escolha == "1":
        return "completo"
    elif escolha == "2":
        return "leve"
    else:
        print(Fore.RED + "Opção inválida!")
        return escolher_tipo_backup()

# =============================
# BACKUP
# =============================

def copiar_pasta(origem, destino):
    if os.path.exists(origem):
        shutil.copytree(origem, destino, dirs_exist_ok=True)

def fazer_backup(base):
    if not verificar_espaco():
        input("\nPressione ENTER para voltar...")
        return

    tipo = escolher_tipo_backup()

    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    temp = os.path.join(DESTINO, f"temp_{data}")

    titulo("BACKUP")

    os.makedirs(temp, exist_ok=True)

    # Pastas principais
    pastas = ["userdata", "config", "appcache"]

    for pasta in pastas:
        src = os.path.join(base, pasta)
        dst = os.path.join(temp, pasta)
        copiar_pasta(src, dst)
        print(Fore.GREEN + f"[OK] {pasta}")

    # Extra: librarycache (horas)
    extra = os.path.join(base, "config", "librarycache")
    if os.path.exists(extra):
        copiar_pasta(extra, os.path.join(temp, "config", "librarycache"))
        print(Fore.GREEN + "[OK] librarycache (horas)")

    # Biblioteca (.acf)
    steamapps = os.path.join(base, "steamapps")
    dest_steamapps = os.path.join(temp, "steamapps")

    if os.path.exists(steamapps):
        os.makedirs(dest_steamapps, exist_ok=True)
        for arq in os.listdir(steamapps):
            if arq.endswith(".acf"):
                shutil.copy2(os.path.join(steamapps, arq), os.path.join(dest_steamapps, arq))
        print(Fore.GREEN + "[OK] Biblioteca")

    # Screenshots (apenas se completo)
    if tipo == "completo":
        screenshots = os.path.join(base, "userdata")
        print(Fore.YELLOW + "[INFO] Screenshots incluídos")
    else:
        print(Fore.YELLOW + "[INFO] Screenshots ignorados")

    # Compactar
    caminho_zip = os.path.join(DESTINO, f"{NOME_ARQUIVO}_{data}")
    shutil.make_archive(caminho_zip, 'zip', temp)
    os.rename(caminho_zip + ".zip", caminho_zip + ".rar")

    shutil.rmtree(temp)

    print(Fore.GREEN + f"\nBackup salvo em:\n{caminho_zip}.rar")

# =============================
# IMPORTAÇÃO
# =============================

def copiar_conteudo(origem, destino):
    if not os.path.exists(origem):
        return
    os.makedirs(destino, exist_ok=True)
    for item in os.listdir(origem):
        src = os.path.join(origem, item)
        dst = os.path.join(destino, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

def importar_backup():
    titulo("IMPORTAR BACKUP")

    origem = selecionar_pasta()
    if not origem:
        print("Nenhuma pasta selecionada.")
        return

    if "userdata" not in os.listdir(origem):
        print(Fore.RED + "Backup inválido!")
        return

    destino = procurar_steam()
    if not destino:
        destino = escolher_pasta()

    fechar_steam()
    titulo("IMPORTANDO...")

    for pasta in ["userdata", "config", "appcache"]:
        copiar_conteudo(os.path.join(origem, pasta), os.path.join(destino, pasta))

    # Biblioteca
    origem_steamapps = os.path.join(origem, "steamapps")
    destino_steamapps = os.path.join(destino, "steamapps")

    if os.path.exists(origem_steamapps):
        os.makedirs(destino_steamapps, exist_ok=True)
        for arq in os.listdir(origem_steamapps):
            if arq.endswith(".acf"):
                shutil.copy2(os.path.join(origem_steamapps, arq), os.path.join(destino_steamapps, arq))
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
            else:
                print(Fore.RED + "Steam não encontrada!")

        elif op == "2":
            base = escolher_pasta()
            fazer_backup(base)

        elif op == "3":
            importar_backup()

        else:
            print(Fore.RED + "Opção inválida!")

        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()
