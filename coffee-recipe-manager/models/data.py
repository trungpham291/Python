from pymongo import MongoClient
from PIL import Image, ImageTk
import random
import os

# Kết nối MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['coffee_recipe_manager']
feedback_collection = db['feedback']

# Dữ liệu mẫu về các món cà phê
categories = [
    {"id": 1, "name": "Espresso"},
    {"id": 2, "name": "Latte"},
    {"id": 3, "name": "Cappuccino"},
    {"id": 4, "name": "Iced Coffee"},
]

recipes = [
    {"id": 1, "name": "Espresso", "categoryId": 1, "ingredients": "Coffee, Water", "steps": "Brew at high pressure.", "time": "5 min", "serves": "1", "image": "coffee1.jpeg"},
    {"id": 2, "name": "Latte", "categoryId": 2, "ingredients": "Espresso, Steamed Milk", "steps": "Pour espresso, add steamed milk.", "time": "10 min", "serves": "1", "image": "coffee2.jpeg"},
    {"id": 3, "name": "Cappuccino", "categoryId": 3, "ingredients": "Espresso, Steamed Milk, Foam", "steps": "Pour espresso, add steamed milk and foam.", "time": "10 min", "serves": "1", "image": "coffee3.jpeg"},
    {"id": 4, "name": "Black Coffee", "categoryId": 4, "ingredients": "Coffee, Water", "steps": "Brew coffee.", "time": "5 min", "serves": "1", "image": "coffee4.jpeg"},
]
def get_random_image():
    # Lựa chọn từ 4 ảnh có sẵn
    image_files = [f"coffee{i}.jpeg" for i in range(1, 5)]  # Chỉ sử dụng coffee1.jpeg, coffee2.jpeg, coffee3.jpeg, coffee4.jpeg
    image_file = random.choice(image_files)  # Chọn ngẫu nhiên 1 ảnh
    image_path = os.path.join("coffee-recipe-manager/images", image_file)  # Đảm bảo đường dẫn đúng
    
    try:
        img = Image.open(image_path).resize((200, 100), Image.LANCZOS)  # Thay đổi kích thước ảnh
        return ImageTk.PhotoImage(img)  # Trả về ảnh
    except FileNotFoundError:
        print(f"Error: Image file {image_path} not found.")  # In thông báo lỗi nếu ảnh không tìm thấy
        return None  # Trả về None nếu không tìm thấy ảnh
def get_feedbacks(recipe_name):
    return list(feedback_collection.find({"recipeId": recipe_name}))  # Truy vấn các góp ý theo tên món
def save_feedback(recipe_name, feedback_text):
    feedback_data = {"recipeId": recipe_name, "feedback": feedback_text}
    feedback_collection.insert_one(feedback_data)  # Lưu vào MongoDB