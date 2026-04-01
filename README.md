# 🚀 SteamVault Backup (LuaTools)
---
Uma ferramenta simples, rápida e eficiente para fazer backup e restauração dos dados da Steam + LuaTools 💾

## 📌 Sobre o projeto

O SteamVault Backup foi criado para preservar com precisão os dados essenciais da Steam, incluindo integração com o LuaTools.

✔ Ideal para:

* Evitar perda de dados ⚠️
* Backup antes de formatar o PC 💻
* Migrar contas entre PCs 🔄
* Preservar biblioteca modificada via LuaTools 🎮
* ✨ Funcionalidades
* 🔍 Detecção automática da Steam (todos os discos)
* 👤 Suporte a múltiplas contas
* 📁 Seleção manual da pasta
* 💾 Backup limpo (somente dados essenciais)
* 📦 Compactação opcional (.zip)
* 📥 Importação automática
* 🔄 Fecha e reabre a Steam
* 📊 Barra de progresso
* 🎨 Interface colorida no terminal
* ⚡ Executável .exe
* 🧠 Como funciona
* 📤 Backup
---
O programa copia somente o necessário:
```
userdata/            → saves, conquistas, horas, screenshots
config/stplug-in     → dados do LuaTools
appcache/stats       → estatísticas da Steam
```
---
✔ Backup fiel ao funcionamento do Steam Tools (LuaTools)

## 📥 Importar (Restaurar)
Selecione a pasta do backup (ou extraída do .zip)

✔ O programa automaticamente:

* Fecha a Steam 🔴
* Restaura os dados 📂
* Reabre a Steam 🟢
---
```
📂 Estrutura do projeto
Steam-Tools_Backup/
│
├── code/
│   ├── project.py
│   ├── requirements.txt
│   ├── run.bat
│   └── site.url
│
├── project.exe
└── README.md
```
---
## ✔ Pré-requisitos
### 🐍Baixe Python

👉 https://www.python.org

✔ Marque: Add Python to PATH

⚙️ Instalar LuaTools

Abra o PowerShell como administrador e execute:
```
irm steam.run | iex
```
* Em seguida:
```
iwr -useb "https://luatools.vercel.app/install-plugin.ps1" | iex
```
---
## ▶️ Como usar
* 🔥 Método recomendado (.exe)

Execute:
```
project.exe
```

👉 Clique com botão direito → Executar como administrador

* 🧪 Método com Python

Execute como administrador:
```
run.bat
```
---
## 🧪 Opções do programa
### 🔹 1 - Backup automático
Detecta a Steam automaticamente
### 🔹 2 - Backup manual
Permite colocar a pasta Steam manualmente
### 🔹 3 - Importar backup
Restaura automaticamente os dados
---
## 📦 Resultado

O backup será salvo em:
```
C:\Users\SEU_USUARIO\Downloads
```

Nome:
```
SteamVault_Backup_DATA.zip
```
---
## ⚠️ Observações
* ❌ NÃO selecione o .zip direto
* ✅ Extraia antes
* ✅ Selecione a pasta extraída
* ⚠️ Deve conter userdata
* 🔄 Steam será fechada automaticamente
* 💡 Não inclui jogos instalados
* 🛠 Tecnologias utilizadas
* Python 🐍
* colorama 🎨
* shutil 📦
* tkinter 🗂️
---
### 🚀 Futuro
* Interface gráfica (GUI)
* Ícone estilo Steam
* Backup automático
* Sistema de profiles
---
## 👨‍💻 Autor

### Brunao916 😎🔥

### ⭐ ApoieSe gostou;

* 👉 Deixe uma ⭐
* 👉 Compartilhe
* 👉 Sugira melhorias
