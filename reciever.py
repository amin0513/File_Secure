import socket
from Crypto.Cipher import AES


key = b"RhombixTechnolog"  

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen(1)

print("Server is listening...")

try:
    while True:
        conn, addr = server.accept()
        print(f"Connection established with {addr}")

        try:
            
            filename = conn.recv(1024).decode()
            conn.send(b"ACK")  
            file_size = int(conn.recv(1024).decode())
            conn.send(b"ACK")
            nonce = conn.recv(16)  
            conn.send(b"ACK") 
            tag = conn.recv(16) 
            conn.send(b"ACK") 

            encrypted_data = b""
            while True:
                chunk = conn.recv(8192)
                if chunk.endswith(b"<end>"):
                    encrypted_data += chunk[:-5]  
                    break
                encrypted_data += chunk

  
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            try:
                decrypted_data = cipher.decrypt_and_verify(encrypted_data, tag)
                print(f"Decryption successful. Saving file as {filename}.")

    
                with open(f"received_{filename}", "wb") as f:
                    f.write(decrypted_data)

            except ValueError:
                print("Decryption failed. Integrity check failed.")

        finally:
            conn.close()
            print(f"Connection with {addr} closed.")

except KeyboardInterrupt:
    print("Server shutting down.")

finally:
    server.close()
