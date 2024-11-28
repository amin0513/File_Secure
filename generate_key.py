from Crypto.Cipher import AES

key = b"RhombixTechnolog" 

cipher = AES.new(key, AES.MODE_EAX)

plaintext = b"Suffain the AI expert"
ciphertext, tag = cipher.encrypt_and_digest(plaintext)

print(f"Ciphertext: {ciphertext}")
print(f"Nonce: {cipher.nonce}")  

# Decrypting the message
cipher_dec = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)
decrypted_text = cipher_dec.decrypt(ciphertext)

print(f"Decrypted text: {decrypted_text.decode()}")
