import tkinter as tk

class CategoryScreen:
    def __init__(self, root, controller):
        self.frame = tk.Frame(root, bg="#fff3e0")
        self.controller = controller

        tk.Label(self.frame, text="Categories", font=("Helvetica", 36, "bold"),
                 bg="#fff3e0", fg="#f39c12").pack(pady=50)

        self.category_list = tk.Frame(self.frame, bg="#fff3e0")
        self.category_list.pack(pady=20)

        for category in self.controller.get_categories():
            btn = tk.Button(self.category_list, text=category["name"], font=("Helvetica", 18),
                            bg="#ffffff", fg="#2c3e50", relief="flat", padx=40, pady=20,
                            command=lambda cid=category["id"]: self.controller.show_recipes(cid))
            btn.pack(fill="x", pady=15, padx=50)
