import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button

# Kích thước bàn cờ
BOARD_SIZE = 10

class CaroGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Cờ Caro - Tkinter")
        self.root.configure(bg="#D4E6F1")  # Nền xanh nhẹ
        
        # Đặt cửa sổ chính ở giữa màn hình
        self.center_window(self.root, 500, 600)
        
        # Biến trạng thái bàn cờ
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = "X"
        
        # Frame chứa bàn cờ
        self.board_frame = tk.Frame(self.root, bg="#5DADE2", bd=5, relief="ridge")
        self.board_frame.pack(pady=20)
        
        # Thêm nhãn hiển thị lượt chơi
        self.turn_label = tk.Label(self.root, text="🔴 Lượt của: X", font=("Arial", 14, "bold"), bg="#D4E6F1", fg="black")
        self.turn_label.pack()
        
        # Giao diện bàn cờ
        self.buttons = []
        for i in range(BOARD_SIZE):
            row_buttons = []
            for j in range(BOARD_SIZE):
                btn = tk.Button(self.board_frame, text="", font=("Arial", 20, "bold"), width=1, height=1,
                                bg="#FDFEFE", fg="black", relief="flat", bd=3,
                                command=lambda row=i, col=j: self.make_move(row, col))
                
                # Hiệu ứng hover
                btn.bind("<Enter>", lambda event, b=btn: b.config(bg="#AED6F1"))
                btn.bind("<Leave>", lambda event, b=btn: b.config(bg="#FDFEFE"))
                
                btn.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        # Frame chứa nút
        self.button_frame = tk.Frame(self.root, bg="#D4E6F1")
        self.button_frame.pack(pady=10)
        
        # Nút Chơi lại
        self.reset_button = self.create_stylish_button("🔄 Chơi lại", self.reset_game, "#1ABC9C", "#16A085", "black")
        self.reset_button.pack(side="left", padx=10)
    
    def create_stylish_button(self, text, command, bg_color, hover_color, text_color):
        """Tạo nút với hiệu ứng hover và thiết kế đẹp"""
        btn = tk.Button(self.button_frame, text=text, font=("Arial", 14, "bold"), command=command,
                        bg=bg_color, fg=text_color, activebackground=hover_color, relief="flat", bd=5, padx=10, pady=5)
        
        # Hiệu ứng hover
        btn.bind("<Enter>", lambda event, b=btn: b.config(bg=hover_color))
        btn.bind("<Leave>", lambda event, b=btn: b.config(bg=bg_color))
        
        return btn
    
    def center_window(self, window, width, height):
        """Căn giữa cửa sổ ứng dụng"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def make_move(self, row, col):
        """Xử lý khi một ô trên bàn cờ được nhấn"""
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, fg="red" if self.current_player == "X" else "blue")
            
            # Kiểm tra thắng cuộc
            if self.check_winner(row, col):
                self.show_winner_popup()
                return
            
            # Chuyển lượt
            self.current_player = "O" if self.current_player == "X" else "X"
            self.update_turn_label()
    
    def update_turn_label(self):
        """Cập nhật nhãn hiển thị lượt chơi"""
        color = "🔴" if self.current_player == "X" else "🔵"
        self.turn_label.config(text=f"{color} Lượt của: {self.current_player}")
    
    def check_winner(self, row, col):
        """Kiểm tra có 5 ký tự liên tiếp thắng không"""
        player = self.board[row][col]
        
        # Kiểm tra 4 hướng chính
        return (self.check_line(row, col, 0, 1, player) or  # Dọc
                self.check_line(row, col, 1, 0, player) or  # Ngang
                self.check_line(row, col, 1, 1, player) or  # Chéo \
                self.check_line(row, col, 1, -1, player))   # Chéo /
    
    def check_line(self, row, col, dr, dc, player):
        """Kiểm tra xem có ít nhất 5 quân liên tiếp theo một hướng cụ thể hay không"""
        count = 1  # Số quân liên tiếp tính từ (row, col)
        
        # Duyệt theo hướng (dr, dc)
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Duyệt theo hướng ngược lại (-dr, -dc)
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        return count >= 5  # Thắng nếu có ít nhất 5 quân liên tiếp
    
    def show_winner_popup(self):
        """Hiển thị thông báo khi có người thắng"""
        popup = Toplevel(self.root)
        popup.title("🎉 Chúc mừng!")
        self.center_window(popup, 350, 200)
        popup.configure(bg="lightyellow")
        
        frame = tk.Frame(popup, bg="gold", bd=5, relief="ridge")
        frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        label = Label(frame, text=f"🏆 Người chơi {self.current_player} thắng! 🎉", font=("Arial", 14, "bold"), bg="gold", fg="darkred", padx=10, pady=10)
        label.pack()
        
        close_button = Button(frame, text="OK", font=("Arial", 12, "bold"), command=lambda: [popup.destroy(), self.reset_game()], bg="black", fg="white")
        close_button.pack(pady=10)
    
    def reset_game(self):
        """Xóa bàn cờ để chơi lại"""
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.board[i][j] = ""
                self.buttons[i][j].config(text="", bg="#FDFEFE")
        self.current_player = "X"
        self.update_turn_label()

root = tk.Tk()
game = CaroGame(root)
root.mainloop()
