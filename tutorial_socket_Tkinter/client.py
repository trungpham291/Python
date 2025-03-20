import socket 
import tkinter as tk 
from threading import Thread 
# Hàm gửi tin nhă ́n
def send_message(): 
    message = entry.get() 
    if message: 
        client_socket.send(message.encode()) 
        text_area.insert(tk.END, "Bạn: " + message + "\n") 
        entry.delete(0, tk.END) 
# Hàm nhận tin nhă ́n từ server
def receive_messages(): 
    while True: 
        try: 
            response = client_socket.recv(1024).decode() 
            text_area.insert(tk.END, "Server: " + response + "\n") 
        except: 
            break
 # Thiê ́t lập socket client 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = '127.0.0.1' 
port = 12345 
client_socket.connect((host, port)) 
# Thiê ́t lập giao diện Tkinter 
window = tk.Tk() 
window.title("Chat Client - Đặng Kim Thi") 
text_area = tk.Text(window, height=10, width=50) 
text_area.pack(pady=10) 
entry = tk.Entry(window, width=40) 
entry.pack(pady=5) 
send_button = tk.Button(window, text="Gư ̉i", command=send_message) 
send_button.pack(pady=5) 
# Khơ ̉i động luô ̀ng nhận tin nhă ́n 
receive_thread = Thread(target=receive_messages) 
receive_thread.daemon = True 
receive_thread.start() 
# Chạy giao diện 
window.mainloop() 
# Đóng socket khi thoát 
client_socket.close()        