from cryptography.fernet import Fernet
import os
# Use this script to encrypt the system messages

# Step 2: Generate and Save Encryption Key (Only once)
key = Fernet.generate_key()
with open("key.key", "wb") as key_file:
    key_file.write(key)

# Step 3: Initialize the Fernet Class
cipher_suite = Fernet(key)

# Step 4: Function to Encrypt File
def encrypt_file(file_path, cipher):
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = cipher.encrypt(file_data)
    with open(f"{file_path}.enc", "wb") as file:
        file.write(encrypted_data)

# Step 5: Loop Through Each Folder and Apply Encryption
folders_to_encrypt = [
    "C:\\Users\\T430\\09-chadtdt\\01a-processing-files-originals-for-encrypt\\01-split-sys-msg-method\\template-version",
    "C:\\Users\\T430\\09-chadtdt\\01a-processing-files-originals-for-encrypt\\02-simple-method\\template-version",
]

for folder in folders_to_encrypt:
    for root, dirs, files in os.walk(folder):
        for file in files:
            if not file.endswith('.enc'):  # Skip already encrypted files
                file_path = os.path.join(root, file)
                encrypt_file(file_path, cipher_suite)
