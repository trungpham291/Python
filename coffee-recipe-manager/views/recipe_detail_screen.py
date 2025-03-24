import tkinter as tk
from tkinter import scrolledtext, messagebox
from models.data import get_random_image, save_feedback, get_feedbacks

class RecipeDetailScreen:
    def __init__(self, root, controller):
        self.frame = tk.Frame(root, bg="#fff3e0")  # Khung với màu nền vàng nhạt
        self.controller = controller

        # Tạo Canvas và Scrollbar
        self.canvas = tk.Canvas(self.frame, bg="#fff3e0")
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Khung chứa các phần tử trong Canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg="#fff3e0")
        self.scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Đặt Scrollbar và Canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Khung nút Back to Category và Back to Home ở góc trái
        button_frame = tk.Frame(self.scrollable_frame, bg="#fff3e0")
        button_frame.grid(row=0, column=0, pady=20, padx=10, sticky="w")  # Đặt vào góc trên bên trái
        tk.Button(button_frame, text="Back to Category", font=("Helvetica", 11), bg="#ecf0f1", fg="#2c3e50", relief="flat", command=self.controller.show_categories, padx=20, pady=10).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Back to Home", font=("Helvetica", 11), bg="#ecf0f1", fg="#2c3e50", relief="flat", command=self.controller.show_welcome, padx=20, pady=10).grid(row=0, column=1, padx=10)

        # Các phần còn lại của giao diện
        self.detail_name = tk.Label(self.scrollable_frame, font=("Helvetica", 28, "bold"), bg="#fff3e0", fg="#f39c12")  # Tiêu đề món
        self.detail_name.grid(row=1, column=0, pady=20, padx=20, sticky="w")

        self.detail_image = tk.Label(self.scrollable_frame, bg="#fff3e0", borderwidth=2, relief="solid")  # Hiển thị ảnh
        self.detail_image.grid(row=2, column=0, pady=10, padx=10)

        self.detail_info_frame = tk.Frame(self.scrollable_frame, bg="#fff3e0")  # Khung thông tin
        self.detail_info_frame.grid(row=3, column=0, pady=10, padx=30, sticky="w")
        tk.Label(self.detail_info_frame, text="Time: ", font=("Helvetica", 14), fg="#2c3e50", bg="#fff3e0").grid(row=0, column=0)
        self.detail_time = tk.Label(self.detail_info_frame, font=("Helvetica", 14), fg="#2c3e50", bg="#fff3e0")
        self.detail_time.grid(row=0, column=1, padx=5)
        tk.Label(self.detail_info_frame, text=" | Serves: ", font=("Helvetica", 14), fg="#2c3e50", bg="#fff3e0").grid(row=0, column=2)
        self.detail_serves = tk.Label(self.detail_info_frame, font=("Helvetica", 14), fg="#2c3e50", bg="#fff3e0")
        self.detail_serves.grid(row=0, column=3, padx=5)

        self.detail_ingredients = tk.Label(self.scrollable_frame, text="Ingredients: ", font=("Helvetica", 16, "bold"), fg="#2c3e50", bg="#fff3e0", justify="left")  # Tiêu đề nguyên liệu
        self.detail_ingredients.grid(row=4, column=0, pady=5, sticky="w")
        self.ingredients_text = tk.Label(self.scrollable_frame, font=("Helvetica", 14), fg="#2c3e50", bg="#ffffff", wraplength=600, padx=20, pady=10, justify="left")  # Nội dung nguyên liệu
        self.ingredients_text.grid(row=5, column=0, pady=5, sticky="w")

        self.detail_steps = tk.Label(self.scrollable_frame, text="Steps: ", font=("Helvetica", 16, "bold"), fg="#2c3e50", bg="#fff3e0", justify="left")  # Tiêu đề hướng dẫn
        self.detail_steps.grid(row=6, column=0, pady=5, sticky="w")
        self.steps_text = tk.Label(self.scrollable_frame, font=("Helvetica", 14), fg="#2c3e50", bg="#ffffff", wraplength=600, padx=20, pady=10, justify="left")  # Nội dung hướng dẫn
        self.steps_text.grid(row=7, column=0, pady=5, sticky="w")

        tk.Label(self.scrollable_frame, text="Your Feedback:", font=("Helvetica", 16, "bold"), fg="#2c3e50", bg="#fff3e0").grid(row=8, column=0, pady=10, sticky="w")  # Tiêu đề góp ý
        self.feedback_text = tk.Text(self.scrollable_frame, height=4, width=60, font=("Helvetica", 12), bg="#ffffff", borderwidth=1, relief="flat")  # Ô nhập góp ý
        self.feedback_text.grid(row=9, column=0, pady=10)

        tk.Button(self.scrollable_frame, text="Submit Feedback", font=("Helvetica", 12), bg="#2ecc71", fg="white", relief="flat", command=self.submit_feedback, padx=20, pady=10).grid(row=10, column=0, pady=10)  # Nút gửi góp ý

        tk.Label(self.scrollable_frame, text="Feedbacks:", font=("Helvetica", 16, "bold"), fg="#2c3e50", bg="#fff3e0").grid(row=11, column=0, pady=10, sticky="w")  # Tiêu đề danh sách góp ý
        self.feedback_list = scrolledtext.ScrolledText(self.scrollable_frame, height=8, width=60, font=("Helvetica", 12), bg="#ffffff", relief="flat", borderwidth=1, wrap=tk.WORD)  # Danh sách góp ý
        self.feedback_list.grid(row=12, column=0, pady=10)

        # Cập nhật lại vùng cuộn cho Canvas
        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Cập nhật vùng cuộn

    def update_details(self, recipe):
        self.detail_name.config(text=recipe["name"])  # Cập nhật tên món
        image = self.controller.get_random_image()
        if image:
            self.detail_image.image = image
            self.detail_image.config(image=image)  # Cập nhật ảnh
        self.detail_time.config(text=recipe["time"])  # Cập nhật thời gian
        self.detail_serves.config(text=recipe["serves"])  # Cập nhật khẩu phần
        self.ingredients_text.config(text=recipe["ingredients"])  # Cập nhật nguyên liệu
        self.steps_text.config(text=recipe["steps"])  # Cập nhật hướng dẫn
        self.feedback_text.delete(1.0, tk.END)  # Xóa ô góp ý
        self.feedback_list.delete(1.0, tk.END)  # Xóa danh sách góp ý cũ
        feedbacks = self.controller.get_feedbacks(recipe["name"])  # Lấy danh sách góp ý
        for fb in feedbacks:
            self.feedback_list.insert(tk.END, f"- {fb['feedback']}\n")  # Thêm góp ý vào danh sách

    def submit_feedback(self):
        feedback = self.feedback_text.get(1.0, tk.END).strip()  # Lấy nội dung góp ý
        recipe_name = self.detail_name.cget("text")  # Lấy tên món
        if not feedback:
            messagebox.showwarning("Error", "Please enter your feedback!")  # Cảnh báo nếu trống
            return
        self.controller.save_feedback(recipe_name, feedback)  # Lưu góp ý vào MongoDB
        messagebox.showinfo("Success", "Feedback submitted!")  # Thông báo thành công
        self.feedback_text.delete(1.0, tk.END)  # Xóa ô góp ý
        self.update_details(self.controller.get_recipe_by_id(self.controller.current_recipe_id))  # Cập nhật lại giao diện
