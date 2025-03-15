from models.data import categories, recipes, save_feedback, get_feedbacks, get_random_image
from views.welcome_screen import WelcomeScreen
from views.category_screen import CategoryScreen
from views.recipe_list_screen import RecipeListScreen
from views.recipe_detail_screen import RecipeDetailScreen

class AppController:
    def __init__(self, root):
        """Khởi tạo ứng dụng và các màn hình."""
        self.root = root
        self.root.title("Recipes Manager")
        self.root.geometry("1000x800")
        self.root.configure(bg="#fff3e0")

        self.current_category_id = None  # Lưu ID thể loại hiện tại
        self.current_recipe_id = None  # Lưu ID món ăn hiện tại

        # Khởi tạo các màn hình
        self.welcome_screen = WelcomeScreen(root, self)
        self.category_screen = CategoryScreen(root, self)
        self.recipe_list_screen = RecipeListScreen(root, self)
        self.recipe_detail_screen = RecipeDetailScreen(root, self)

        self.show_welcome()  # Mặc định hiển thị màn hình chào mừng

    def show_frame(self, frame):
        """Ẩn tất cả màn hình và chỉ hiển thị màn hình được chọn."""
        for f in (self.welcome_screen.frame, self.category_screen.frame, 
                  self.recipe_list_screen.frame, self.recipe_detail_screen.frame):
            f.pack_forget()  # Ẩn toàn bộ màn hình
        frame.pack(fill="both", expand=True)  # Hiển thị màn hình được chọn

    def get_categories(self):
        """Lấy danh sách thể loại món ăn từ Model."""
        return categories

    def get_recipes_by_category(self, category_id):
        """Lấy danh sách món ăn theo ID thể loại."""
        return [r for r in recipes if r["categoryId"] == category_id]

    def get_recipe_by_id(self, recipe_id):
        """Lấy chi tiết một món ăn theo ID."""
        return next(r for r in recipes if r["id"] == recipe_id)

    def get_random_image(self):
        """Lấy ảnh món ăn ngẫu nhiên từ thư mục images/."""
        return get_random_image()

    def save_feedback(self, recipe_name, feedback_text):
        """Lưu góp ý vào MongoDB."""
        save_feedback(recipe_name, feedback_text)

    def get_feedbacks(self, recipe_name):
        """Lấy danh sách góp ý từ MongoDB."""
        return get_feedbacks(recipe_name)

    def show_welcome(self):
        """Hiển thị màn hình chào mừng."""
        self.show_frame(self.welcome_screen.frame)

    def show_categories(self):
        """Hiển thị màn hình danh mục món ăn."""
        self.show_frame(self.category_screen.frame)

    def show_recipes(self, category_id):
        """Hiển thị danh sách món ăn theo thể loại."""
        self.current_category_id = category_id  # Cập nhật ID thể loại
        recipes_data = self.get_recipes_by_category(category_id)  # Lấy danh sách món ăn
        self.recipe_list_screen.update_recipes(recipes_data)  # Cập nhật danh sách món
        self.show_frame(self.recipe_list_screen.frame)  # Chuyển đến màn hình danh sách món

    def show_recipe_detail(self, recipe_id):
        """Hiển thị màn hình chi tiết của một món ăn."""
        self.current_recipe_id = recipe_id  # Cập nhật ID món ăn
        recipe = self.get_recipe_by_id(recipe_id)  # Lấy thông tin món ăn
        self.recipe_detail_screen.update_details(recipe)  # Cập nhật giao diện chi tiết món
        self.show_frame(self.recipe_detail_screen.frame)  # Chuyển đến màn hình chi tiết món
