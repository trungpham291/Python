import tkinter as tk

class RecipeListScreen:
    def __init__(self, root, controller):
        self.frame = tk.Frame(root, bg="#fff3e0")
        self.controller = controller

        tk.Label(self.frame, text="Recipes", font=("Helvetica", 36, "bold"),
                 bg="#fff3e0", fg="#f39c12").pack(pady=50)

        self.recipe_list = tk.Frame(self.frame, bg="#fff3e0")
        self.recipe_list.pack(pady=20)

    def update_recipes(self, recipes):
        for widget in self.recipe_list.winfo_children():
            widget.destroy()
        for recipe in recipes:
            frame = tk.Frame(self.recipe_list, bg="#ffffff", borderwidth=1, relief="solid")
            frame.pack(fill="x", pady=10, padx=50)

            image = self.controller.get_random_image()
            if image:
                img_label = tk.Label(frame, image=image, bg="#ffffff")
                img_label.image = image
                img_label.pack(side="left", padx=10)

            tk.Label(frame, text=recipe["name"], font=("Helvetica", 16, "bold"), fg="#2c3e50", bg="#ffffff",
                     wraplength=500).pack(side="left", padx=10, pady=5)

            tk.Button(frame, text="View", font=("Helvetica", 12), bg="#f1c40f", fg="white",
                      relief="flat", command=lambda rid=recipe["id"]: self.controller.show_recipe_detail(rid),
                      padx=15, pady=5).pack(side="right", padx=10)
