import tkinter as tk
from tkinter import scrolledtext, messagebox

class RecipeDetailScreen:
    def __init__(self, root, controller):
        self.frame = tk.Frame(root, bg="#fff3e0")
        self.controller = controller

        # Tiêu đề món ăn
        self.detail_name = tk.Label(self.frame, font=("Helvetica", 28, "bold"),
                                    bg="#fff3e0", fg="#f39c12")
        self.detail_name.pack(pady=20)

        # Hình ảnh món ăn
        self.detail_image = tk.Label(self.frame, bg="#fff3e0", borderwidth=2, relief="solid")
        self.detail_image.pack(pady=10)

        # Khung chứa thời gian và khẩu phần
        self.detail_info_frame = tk.Frame(self.frame, bg="#fff3e0")
        self.detail_info_frame.pack(pady=10, padx=50)
        
        tk.Label(self.detail_info_frame, text="Time:", font=("Helvetica", 14),
                 fg="#2c3e50", bg="#fff3e0").pack(side="left")
        self.detail_time = tk.Label(self.detail_info_frame, font=("Helvetica", 14),
                                    fg="#2c3e50", bg="#fff3e0")
        self.detail_time.pack(side="left", padx=5)

        tk.Label(self.detail_info_frame, text="| Serves:", font=("Helvetica", 14),
                 fg="#2c3e50", bg="#fff3e0").pack(side="left")
        self.detail_serves = tk.Label(self.detail_info_frame, font=("Helvetica", 14),
                                      fg="#2c3e50", bg="#fff3e0")
        self.detail_serves.pack(side="left", padx=5)

        # Tiêu đề và nội dung nguyên liệu
        self.detail_ingredients = tk.Label(self.frame, text="Ingredients:", font=("Helvetica", 16, "bold"),
                                           fg="#2c3e50", bg="#fff3e0", justify="left")
        self.detail_ingredients.pack(pady=5)

        self.ingredients_text = tk.Label(self.frame, font=("Helvetica", 14),
                                         fg="#2c3e50", bg="#ffffff", wraplength=800, padx=20, pady=10, justify="left")
        self.ingredients_text.pack(fill="x", pady=5)

        # Tiêu đề và nội dung hướng dẫn
        self.detail_steps = tk.Label(self.frame, text="Steps:", font=("Helvetica", 16, "bold"),
                                     fg="#2c3e50", bg="#fff3e0", justify="left")
        self.detail_steps.pack(pady=5)

        self.steps_text = tk.Label(self.frame, font=("Helvetica", 14),
                                   fg="#2c3e50", bg="#ffffff", wraplength=800, padx=20, pady=10, justify="left")
        self.steps_text.pack(fill="x", pady=5)

        # Ô nhập góp ý
        tk.Label(self.frame, text="Your Feedback:", font=("Helvetica", 16, "bold"),
                 fg="#2c3e50", bg="#fff3e0").pack(pady=10)
        self.feedback_text = tk.Text(self.frame, height=4, width=60, font=("Helvetica", 12),
                                     bg="#ffffff", borderwidth=1, relief="flat")
        self.feedback_text.pack(pady=10)
        
        tk.Button(self.frame, text="Submit Feedback", font=("Helvetica", 12), bg="#2ecc71", fg="white",
                  relief="flat", command=self.submit_feedback, padx=20, pady=10).pack(pady=10)

        # Danh sách góp ý
        tk.Label(self.frame, text="Feedbacks:", font=("Helvetica", 16, "bold"),
                 fg="#2c3e50", bg="#fff3e0").pack(pady=10)
        self.feedback_list = scrolledtext.ScrolledText(self.frame, height=8, width=60,
                                                       font=("Helvetica", 12), bg="#ffffff", relief="flat",
                                                       borderwidth=1, wrap=tk.WORD)
        self.feedback_list.pack(pady=10)

        # Nút Back to Category và Back to Home
        button_frame = tk.Frame(self.frame, bg="#fff3e0")
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Back to Category", font=("Helvetica", 14), bg="#ecf0f1", fg="#2c3e50",
                  relief="flat", command=self.controller.show_recipes, padx=20, pady=10).pack(side="left", padx=10)
        tk.Button(button_frame, text="Back to Home", font=("Helvetica", 14), bg="#ecf0f1", fg="#2c3e50",
                  relief="flat", command=self.controller.show_welcome, padx=20, pady=10).pack(side="left", padx=10)

    def update_details(self, recipe):
        """Cập nhật giao diện với thông tin chi tiết món ăn."""
        self.detail_name.config(text=recipe["name"])
        
        # Hiển thị hình ảnh ngẫu nhiên
        image = self.controller.get_random_image()
        if image:
            self.detail_image.image = image
            self.detail_image.config(image=image)

        self.detail_time.config(text=recipe["time"])
        self.detail_serves.config(text=recipe["serves"])
        self.ingredients_text.config(text=recipe["ingredients"])
        self.steps_text.config(text=recipe["steps"])

        # Làm mới danh sách góp ý
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_list.delete(1.0, tk.END)

        feedbacks = self.controller.get_feedbacks(recipe["name"])
        for fb in feedbacks:
            self.feedback_list.insert(tk.END, f"- {fb['feedback']}\n")

    def submit_feedback(self):
        """Lưu góp ý từ người dùng vào MongoDB."""
        feedback = self.feedback_text.get(1.0, tk.END).strip()
        recipe_name = self.detail_name.cget("text")

        if not feedback:
            messagebox.showwarning("Error", "Please enter your feedback!")
            return

        self.controller.save_feedback(recipe_name, feedback)
        messagebox.showinfo("Success", "Feedback submitted!")

        # Làm mới giao diện sau khi gửi góp ý
        self.feedback_text.delete(1.0, tk.END)
        self.update_details(self.controller.get_recipe_by_id(self.controller.current_recipe_id))
