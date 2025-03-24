from models.data import categories, recipes, save_feedback, get_feedbacks, get_random_image
from views.welcome_screen import WelcomeScreen
from views.category_screen import CategoryScreen
from views.recipe_list_screen import RecipeListScreen
from views.recipe_detail_screen import RecipeDetailScreen

class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Recipes")
        self.root.geometry("1000x800")
        self.root.configure(bg="#fff3e0")

        self.current_category_id = None
        self.current_recipe_id = None

        self.welcome_screen = WelcomeScreen(root, self)
        self.category_screen = CategoryScreen(root, self)
        self.recipe_list_screen = RecipeListScreen(root, self)
        self.recipe_detail_screen = RecipeDetailScreen(root, self)

        self.show_welcome()

    # Thêm phương thức get_feedbacks
    def get_feedbacks(self, recipe_name):
        return get_feedbacks(recipe_name)  # Gọi hàm get_feedbacks từ model để lấy góp ý

    def save_feedback(self, recipe_name, feedback_text):
        save_feedback(recipe_name, feedback_text)  # Lư
        
    def show_frame(self, frame):
        for f in (self.welcome_screen.frame, self.category_screen.frame, self.recipe_list_screen.frame, self.recipe_detail_screen.frame):
            f.pack_forget()
        frame.pack(fill="both", expand=True)

    def get_categories(self):
        return categories

    def get_recipes_by_category(self, category_id):
        return [r for r in recipes if r["categoryId"] == category_id]

    def get_recipe_by_id(self, recipe_id):
        return next(r for r in recipes if r["id"] == recipe_id)

    def get_random_image(self):
        return get_random_image()

    def show_welcome(self):
        self.show_frame(self.welcome_screen.frame)

    def show_categories(self):
        self.show_frame(self.category_screen.frame)

    def show_recipes(self, category_id):
        self.current_category_id = category_id
        recipes_data = self.get_recipes_by_category(category_id)
        self.recipe_list_screen.update_recipes(recipes_data)
        self.show_frame(self.recipe_list_screen.frame)

    def show_recipe_detail(self, recipe_id):
        self.current_recipe_id = recipe_id
        recipe = self.get_recipe_by_id(recipe_id)
        self.recipe_detail_screen.update_details(recipe)
        self.show_frame(self.recipe_detail_screen.frame)