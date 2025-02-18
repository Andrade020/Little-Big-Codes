# Little-Big-Codes
This is a compilation of very simple code that make your life much easier. It includes routine functions, macros, automation, etc

# CodeSlangify 📝✨

CodeSlangify is a Python-based tool that automatically abbreviates comments and docstrings in Python code, converting them into a more informal and slang-like style. It was originaly made for running with brasilian portuguese, and it works better that way, but  

## Features 🚀

- ✅ **Automatic slang conversion** for comments (`#`) and docstrings (`''' """`).
- ✅ **Smart word abbreviation** based on length and vowels.
- ✅ **Custom slang dictionary** that you can extend.
- ✅ **User-friendly GUI** built with `Tkinter` for easy code processing.

## Installation 🛠️
Python installed, then install the required dependencies:

```bash
pip install tk
```

## How It Works ⚡

1. Enter your Python code into the input box.
2. Click **"Process Code"** to transform the comments and docstrings.
3. View the modified code with shortened comments in the output box.

## Example 🎯

### Before:
```python
# This function calculates the sum of two numbers
def add(a, b):
    """
    This function receives two integers and returns their sum.
    """
    return a + b
```

### After:
```python
# This func calc sum d 2 nums
def add(a, b):
    """
    This func rcv 2 ints nd rtns thr sum.
    """
    return a + b
```

## Customizing the Slang Dictionary 🛠️

You can add your own slang words to the `SLANG_DICT` dictionary in the script. Example:

```python
SLANG_DICT = {
    "function": "func",
    "calculate": "calc",
    "integer": "int",
}
```

## Running the Application ▶️

Run the script:

```bash
python codeslangify.py
```

This will open a graphical interface where you can enter and process Python code.



# SecureIdeas - Encrypted Idea Manager
### 📝 1. Simple Idea Manager (`Ideas.ahk`)
This script allows you to quickly store ideas in a text file.

🔹 **Keyboard Shortcuts:**
- **Ctrl + Win + Alt + I** → Open a box to write an idea.
- **Ctrl + Win + Alt + D** → Add details to the last saved idea.

🔹 **Output Format:**
- Ideas are saved in `C:\Users\Leo\Desktop\Portfolio\Ideas.txt` in the format:
  ```
  MM/DD/YYYY HH:MM - [IDEA]
  Details: [OPTIONAL DETAILS]
  ```

---

### 🔐 2. Secure Idea Manager (`SecureIdeas.ahk`)
This script securely stores ideas by encrypting data with **AES-256**.

🔹 **Keyboard Shortcuts:**
- **Ctrl + Win + Alt + P** → Set the encryption key.
- **Ctrl + Win + Alt + C** → Add an encrypted idea.
- **Ctrl + Win + Alt + O** → Decrypt and view ideas.

🔹 **Secure Storage:**
- Ideas are encrypted and stored in `C:\Users\Leo\Desktop\Portfolio\Crypt.txt`.
- The encryption key must be entered to view the ideas.
- The password is protected using **SHA-256 hashing**, preventing resets without the original password.

⚠️ **IMPORTANT:**
- The script **does not store the original password**, only its hash.
- Without the correct password, data cannot be recovered.

---

## 🛠 Installation & Usage

### 🔹 **Step 1: Install AutoHotkey**
Download and install **AutoHotkey** from the official website:
👉 [https://www.autohotkey.com/](https://www.autohotkey.com/)

### 🔹 **Step 2: Install OpenSSL (for encryption)**
The secure script requires **OpenSSL** for AES-256 encryption. You can download it here:
👉 [https://slproweb.com/products/Win32OpenSSL.html](https://slproweb.com/products/Win32OpenSSL.html)

After installation, add the OpenSSL path to the Windows `PATH` so AutoHotkey can use it.

### 🔹 **Step 3: Run the Script**
1. **Download or copy** the code into an `.ahk` file.
2. **Double-click** the `.ahk` file to run the script.
3. **Use the shortcuts** to add and view your ideas!

---

## 🛡 Additional Security
To enhance the security of the encrypted script, you can:
- **Store `password.txt` in a protected location** or on a separate USB drive.
- **Use a password manager** to keep your master password safe.
- **Encrypt `password.txt` itself** using a tool like VeraCrypt.

---

---


## 🔒 Overview
SecureIdeas is an AutoHotkey (AHK) script that securely stores and retrieves encrypted ideas using AES-256 encryption. The encryption key must be entered every time an idea is saved or retrieved, ensuring that only authorized users can access the stored information.

## 🚀 Features
- **AES-256 Encryption:** Encrypts all stored ideas to keep them secure.
- **Master Password Protection:** Requires a password for encryption and decryption.
- **Automatic Timestamping:** Saves ideas with a timestamp in `MM/DD/YYYY HH:MM` format.
- **Secure Storage:** Uses OpenSSL for encryption and decryption.
- **Hotkeys for Quick Access:**
  - Open the first time : Set the master password (only on the first run).
  - `Ctrl + Win + Alt + C`: Save a new encrypted idea.
  - `Ctrl + Win + Alt + O`: Decrypt and display stored ideas.

## 🔧 Requirements
- **AutoHotkey**: Install [AutoHotkey](https://www.autohotkey.com/) to run the script.
- **OpenSSL**: Ensure OpenSSL is installed and accessible from the command line.
  - Windows users can download OpenSSL from [here](https://slproweb.com/products/Win32OpenSSL.html).
  - Alternatively, if you have Git for Windows installed, you can use OpenSSL from `C:\Program Files\Git\usr\bin\openssl.exe`.

## 🛠️ Installation
1. Install AutoHotkey.
2. Install OpenSSL and add it to your system's PATH.
3. Save the script as `SecureIdeas.ahk`.
4. Run the script.
5. Set your master password (only required on first run).
6. Use the hotkeys to save and retrieve encrypted ideas.

## 🔑 How It Works
1. **First Time Setup:**
   - The script asks you to set a **master password**.
   - The password's SHA-256 hash is stored in `password.txt` (not the actual password).
2. **Saving an Idea (`Ctrl + Win + Alt + I`)**
   - The user enters their password.
   - If correct, they can input an idea.
   - The idea is encrypted with AES-256 and stored in `Crypt.txt`.
3. **Retrieving Ideas (`Ctrl + Win + Alt + D`)**
   - The user enters their password.
   - If correct, the script decrypts and displays the stored ideas.

## 🔐 Security Considerations
- The **password is never stored in plain text**, only its SHA-256 hash is saved.
- If you forget your password, **you cannot recover your data**.
- For extra security, store `password.txt` in a secure location or encrypt it using an external tool like **VeraCrypt**.

## 💡 Future Enhancements
- Implement a GUI for better user experience.
- Add optional cloud backup with encryption.
- Provide an option to change the master password securely.



---

Enjoy secure idea storage! 😊🔐



# 📜 AutoHotkey Idea Manager

Este repositório contém dois scripts em **AutoHotkey (AHK)** para gerenciar suas ideias. Um deles é um **gerenciador simples de ideias**, enquanto o outro é um **gerenciador seguro com criptografia AES-256**.

---

## 🚀 Scripts Disponíveis

### 📝 1. Gerenciador de Ideias Simples (`Ideas.ahk`)
Este script permite armazenar rapidamente ideias em um arquivo de texto.

🔹 **Atalhos de Teclado:**
- **Ctrl + Win + Alt + I** → Abrir caixa para escrever uma ideia.
- **Ctrl + Win + Alt + D** → Adicionar detalhes à última ideia salva.

🔹 **Saída:**
- As ideias são salvas em `C:\Users\Leo\Desktop\Portfolio\Ideas.txt` no formato:
  ```
  MM/DD/YYYY HH:MM - [IDEIA]
  Detalhes: [DETALHES OPCIONAIS]
  ```

---

### 🔐 2. Gerenciador Seguro de Ideias (`SecureIdeas.ahk`)
Este script armazena ideias de forma segura, criptografando os dados com **AES-256**.

🔹 **Atalhos de Teclado:**
- **Ctrl + Win + Alt + P** → Definir a chave de criptografia.
- **Ctrl + Win + Alt + C** → Adicionar uma ideia criptografada.
- **Ctrl + Win + Alt + O** → Descriptografar e visualizar as ideias.

🔹 **Armazenamento Seguro:**
- As ideias são salvas criptografadas no arquivo `C:\Users\Leo\Desktop\Portfolio\Crypt.txt`.
- A chave de criptografia precisa ser digitada para visualizar as ideias.
- A senha é protegida com **hash SHA-256**, impedindo redefinições sem a senha original.

⚠️ **IMPORTANTE:**
- O script **não armazena a senha original**, apenas seu hash.
- Sem a senha correta, não há como recuperar os dados.

---

## 🛠 Instalação e Uso

### 🔹 **Passo 1: Instale o AutoHotkey**
Baixe e instale o **AutoHotkey** no site oficial:
👉 [https://www.autohotkey.com/](https://www.autohotkey.com/)

### 🔹 **Passo 2: Instale o OpenSSL (para criptografia)**
O script seguro requer **OpenSSL** para realizar a criptografia AES-256. Você pode baixá-lo aqui:
👉 [https://slproweb.com/products/Win32OpenSSL.html](https://slproweb.com/products/Win32OpenSSL.html)

Após a instalação, adicione o caminho do OpenSSL ao `PATH` do Windows para que o AutoHotkey possa usá-lo.

### 🔹 **Passo 3: Execute o Script**
1. **Baixe ou copie** o código para um arquivo `.ahk`.
2. **Dê um duplo clique** no arquivo `.ahk` para rodar o script.
3. **Use os atalhos** para adicionar e visualizar suas ideias!

---

## 🛡 Segurança Adicional
Se quiser aumentar a segurança do script seguro, você pode:
- **Armazenar `password.txt` em um local protegido** ou usá-lo em um pendrive separado.
- **Usar um gerenciador de senhas** para guardar sua senha mestra.
- **Criptografar o próprio arquivo `password.txt`** com uma ferramenta como VeraCrypt.

---


