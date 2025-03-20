import socket 
# Thiê ́t lập thông tin server 
host = '127.0.0.1'  # Địa chi ̉ IP cu ̉a server (localhost) 
port = 12345        
# Cô ̉ng mà server sẽ lă ́ng nghe 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# Liên kêt và lăng nghe kêt nôi 
server_socket.bind((host, port)) 
server_socket.listen(1) 
print("Server đang lă ́ng nghe tại", host, ":", port) 
# Châ ́p nhận kê ́t nô ́i từ client 
client_socket, addr = server_socket.accept() 
print("Đã kê ́t nô ́i với", addr) 
# Vòng lặp đê ̉ nhận và gửi tin nhă ́n
while True: 
    data = client_socket.recv(1024).decode() 
    if not data:
        break 
    print("Client gửi:", data) 
    client_socket.send("Tin nhăn đã được nhận!".encode()) 
# Đóng kê ́t nô ́i 
client_socket.close() 
server_socket.close() 