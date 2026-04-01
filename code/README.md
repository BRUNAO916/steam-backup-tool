# 🚀 Steam-Tools_Backup

Uma ferramenta simples, rápida e eficiente para fazer **backup e restauração dos saves da Steam automaticamente** 💾

---

## 📌 Sobre o projeto

O **Steam-Tools_Backup** foi criado para facilitar o backup e a recuperação de dados importantes da Steam, como saves, configurações e estatísticas.

✔ Ideal para:

* Evitar perda de dados ⚠️
* Fazer backup antes de formatar o PC 💻
* Migrar arquivos entre computadores 🔄

---

## ✨ Funcionalidades

* 🔍 Detecção automática da Steam
* 📁 Seleção manual da pasta
* 💾 Backup completo dos arquivos
* 📦 Geração de arquivo compactado (.rar)
* 📥 Importação de backup com 1 clique
* 🔄 Fecha e reabre a Steam automaticamente
* 🎨 Interface colorida no terminal
* ⚡ Execução rápida via `.exe`

---

## 🧠 Como funciona

### 📤 Backup

O programa:

1. Localiza a pasta da Steam
2. Copia os diretórios importantes:

   * `appcache/stats`
   * `config/stplug-in`
   * `userdata`
3. Cria um backup temporário
4. Compacta tudo em um arquivo
5. Salva em **Downloads**

---

### 📥 Importar (Restaurar)

1. Selecione a pasta do backup extraído:
Steam-Tools_Backup_XXXX-XX-XX_XX-XX-XX

✔ O programa automaticamente:

* Fecha a Steam 🔴
* Restaura os arquivos 📂
* Abre a Steam novamente 🟢

---

## 📂 Estrutura do projeto
```
Steam-Tools_Backup/
│
├── steambackup.exe   # Executável (uso direto)
├── project.py        # Código principal
├── run.bat           # Executar via Python
├── requirements.txt  # Dependências
└── README.md         # Documentação
```

---

## ✔ Pré-requisitos

### ⚙️ Instalação

###  1. 🐍Instalar Python 

Baixe aqui:
👉 https://www.python.org

✔ Marque: **Add Python to PATH**

### 2. 🌑Instlar o LuaTools

* Abra o powershell como adm e cole:
```
irm steam.run | iex
iwr -useb "https://luatools.vercel.app/install-plugin.ps1" | iex
```

---

## ▶️ Como usar

* Clique duas vezes em:
```
run.bat
```

(Na primeira execução, ele pode demorar um pouco, pois está instalando o Python e os Plugins necessários caso não tenha ainda).

---

## 🧪 Opções do programa

Ao iniciar, você pode escolher:

### 🔹 1 - Automático

Procura a Steam automaticamente no sistema

### 🔹 2 - Manual

Você digita o caminho da pasta
Exemplos:
C:\Program Files (x86)\Steam
D:\Program Files (x86)\Steam

### 🔹 3 - Importar backup

* Seleciona a pasta do backup e restaura automaticamente os seus saves

---

## 📦 Resultado

* O seu save estara salvo em downloads disco C:\

Com o nome:
```
Steam-Tools_Backup_DATA.rar
```

---

## ⚠️ Observações

* ❌ Não selecione o arquivo `.rar` ao importar
Antes extraia o arquivo com o winrar
Baixe-o aqui 👉 https://www.win-rar.com/
* ✅ Selecione a pasta extraída do backup
* ⚠️ A pasta deve conter `userdata`
* 🔄 A Steam será fechada automaticamente na restauração
* 📦 O arquivo `.rar` é na verdade um `.zip` renomeado
* Alguns caminhos podem variar dependendo da instalação

---

## 🛠 Tecnologias utilizadas

* Python 🐍
* colorama 🎨
* shutil 📦
* tkinter 🗂️

---

## 🚀 Futuras melhorias

* Interface gráfica (GUI) 🖥️
* Barra de progresso 📊
* Backup automático programado ⏰
* Seleção automática do backup mais recente 🤖

---

## 👨‍💻 Autor

Desenvolvido por **Brunao916** 😎🔥

---

## ⭐ Apoie o projeto

Se você gostou, deixe uma ⭐ no repositório!

Isso ajuda muito 🙌
