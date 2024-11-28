import os
import socket
from Crypto.Cipher import AES
import streamlit as st

key = b"RhombixTechnolog"  
cipher = AES.new(key, AES.MODE_EAX)

st.title("Rhombix Technologies File Upload and Encryption")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "jpg", "png", "csv", "zip"])

server_address = ("localhost", 9999) 

if uploaded_file is not None:
    filename = uploaded_file.name
    file_size = uploaded_file.size

 
    file_data = uploaded_file.read()

   
    ciphertext, tag = cipher.encrypt_and_digest(file_data)

    st.write(f"File Name: {filename}")
    st.write(f"File Size: {file_size} bytes")
    st.write("Encrypting and sending file...")

    try:
       
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(server_address)

        client.send(f"{filename}".encode())  
        client.recv(1024) 
        client.send(str(file_size).encode()) 
        client.recv(1024) 
        client.send(cipher.nonce)  
        client.recv(1024)  
        client.send(tag)  
        client.recv(1024)  

        # Send encrypted file data
        chunk_size = 8192  # Define chunk size (8KB)
        for i in range(0, len(ciphertext), chunk_size):
            chunk = ciphertext[i:i + chunk_size]
            client.sendall(chunk)  # Send each chunk of encrypted file data

        # Send end-of-file marker
        client.send(b"<end>")
        st.success("File sent successfully!")

    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        client.close() 
