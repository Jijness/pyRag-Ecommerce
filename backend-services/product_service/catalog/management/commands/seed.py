import random
from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Seed database with 12 product categories and ~10 items each'

    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        Product.objects.all().delete()

        categories_dict = {
            "Sách": [
                ("Sách Clean Code", 250000, {"author": "Robert C. Martin", "pages": 464}),
                ("Sách Đắc Nhân Tâm", 85000, {"author": "Dale Carnegie", "pages": 320}),
                ("Nhà Giả Kim", 75000, {"author": "Paulo Coelho", "pages": 228}),
                ("Tuổi Trẻ Đáng Giá Bao Nhiêu", 80000, {"author": "Rosie Nguyễn", "pages": 285}),
                ("Tâm Lý Học Tội Phạm", 120000, {"author": "Tôn Thất Chương", "pages": 350}),
                ("Sách Thiết kế Hệ thống", 300000, {"author": "Alex Xu", "pages": 400}),
                ("Nghĩ Giàu Làm Giàu", 95000, {"author": "Napoleon Hill", "pages": 300}),
                ("Tiểu thuyết Bố Già", 110000, {"author": "Mario Puzo", "pages": 450}),
                ("Thói quen nguyên tử", 150000, {"author": "James Clear", "pages": 320}),
                ("Lược sử loài người", 180000, {"author": "Yuval Noah Harari", "pages": 500})
            ],
            "Điện thoại": [
                ("iPhone 15 Pro Max", 29000000, {"brand": "Apple", "ram": "8GB", "storage": "256GB"}),
                ("Samsung Galaxy S24 Ultra", 27500000, {"brand": "Samsung", "ram": "12GB", "storage": "512GB"}),
                ("Xiaomi 14 Pro", 18000000, {"brand": "Xiaomi", "ram": "12GB", "storage": "256GB"}),
                ("Oppo Find X7", 20000000, {"brand": "Oppo", "ram": "12GB", "storage": "256GB"}),
                ("iPhone 14 Plus", 20000000, {"brand": "Apple", "ram": "6GB", "storage": "128GB"}),
                ("Samsung Galaxy A54", 8000000, {"brand": "Samsung", "ram": "8GB", "storage": "128GB"}),
                ("Vivo X100", 17500000, {"brand": "Vivo", "ram": "12GB", "storage": "256GB"}),
                ("Realme GT 5", 12000000, {"brand": "Realme", "ram": "16GB", "storage": "512GB"}),
                ("Asus ROG Phone 8", 22000000, {"brand": "Asus", "ram": "16GB", "storage": "512GB"}),
                ("Google Pixel 8 Pro", 25000000, {"brand": "Google", "ram": "12GB", "storage": "128GB"})
            ],
            "Laptop": [
                ("MacBook Pro M3 14inch", 40000000, {"brand": "Apple", "cpu": "M3 Pro", "ram": "18GB"}),
                ("Dell XPS 15", 35000000, {"brand": "Dell", "cpu": "Core i7", "ram": "16GB"}),
                ("ThinkPad X1 Carbon", 38000000, {"brand": "Lenovo", "cpu": "Core i7", "ram": "16GB"}),
                ("Asus Zenbook 14", 25000000, {"brand": "Asus", "cpu": "Ryzen 7", "ram": "16GB"}),
                ("Acer Nitro 5", 18000000, {"brand": "Acer", "cpu": "Core i5", "ram": "8GB"}),
                ("HP Envy x360", 22000000, {"brand": "HP", "cpu": "Core i5", "ram": "8GB"}),
                ("MSI Katana 15", 24000000, {"brand": "MSI", "cpu": "Core i7", "ram": "16GB"}),
                ("LG Gram 16", 32000000, {"brand": "LG", "cpu": "Core i7", "ram": "16GB"}),
                ("MacBook Air M2", 23000000, {"brand": "Apple", "cpu": "M2", "ram": "8GB"}),
                ("Lenovo Legion 5", 28000000, {"brand": "Lenovo", "cpu": "Ryzen 7", "ram": "16GB"})
            ],
            "Thời trang Nam": [
                ("Áo thun T-shirt Basic", 150000, {"size": "L", "material": "Cotton 100%"}),
                ("Quần Jeans Slimfit", 350000, {"size": "32", "material": "Denim"}),
                ("Áo sơ mi Oxford", 250000, {"size": "XL", "material": "Cotton"}),
                ("Áo khoác Bomber", 450000, {"size": "L", "material": "Polyester"}),
                ("Quần Kaki dạo phố", 280000, {"size": "31", "material": "Kaki"}),
                ("Giày Sneaker thể thao", 550000, {"size": "42", "brand": "Nike"}),
                ("Áo Polo phong cách", 220000, {"size": "M", "material": "Cá sấu"}),
                ("Quần short đi biển", 120000, {"size": "L", "material": "Nylon"}),
                ("Áo Len cổ lọ", 300000, {"size": "L", "material": "Len"}),
                ("Mũ lưỡi trai", 80000, {"size": "Freesize", "brand": "Adidas"})
            ],
            "Thời trang Nữ": [
                ("Váy hoa nhí", 250000, {"size": "S", "material": "Voan"}),
                ("Áo Croptop", 120000, {"size": "M", "material": "Cotton"}),
                ("Quần ống rộng", 220000, {"size": "L", "material": "Đũi"}),
                ("Áo sơ mi lụa", 280000, {"size": "S", "material": "Lụa"}),
                ("Chân váy chữ A", 150000, {"size": "M", "material": "Kaki"}),
                ("Đầm dự tiệc", 450000, {"size": "M", "material": "Ren"}),
                ("Túi xách da nữ", 350000, {"brand": "Local Brand", "material": "Da PU"}),
                ("Giày cao gót 5cm", 250000, {"size": "37", "color": "Đen"}),
                ("Áo len mỏng", 180000, {"size": "Freesize", "material": "Len tăm"}),
                ("Phụ kiện Khuyên tai", 50000, {"material": "Bạc 925"})
            ],
            "Đồ gia dụng": [
                ("Nồi chiên không dầu", 2100000, {"capacity": "6.2L", "brand": "Philips"}),
                ("Lò vi sóng", 1500000, {"capacity": "20L", "brand": "Sharp"}),
                ("Máy ép trái cây chậm", 1800000, {"brand": "Panasonic", "warranty": "12 tháng"}),
                ("Máy hút bụi cầm tay", 950000, {"brand": "Xiaomi", "power": "500W"}),
                ("Robot hút bụi", 6500000, {"brand": "Roborock", "battery": "5200mAh"}),
                ("Bàn ủi hơi nước", 450000, {"brand": "Sunhouse", "power": "1200W"}),
                ("Bếp từ đôi", 3200000, {"brand": "Kangaroo", "power": "4000W"}),
                ("Máy lọc không khí", 2800000, {"brand": "Xiaomi", "filter": "HEPA"}),
                ("Bình đun siêu tốc", 250000, {"brand": "Philips", "capacity": "1.7L"}),
                ("Nồi cơm điện cao tần", 2500000, {"brand": "Toshiba", "capacity": "1.8L"})
            ],
            "Đồ chơi": [
                ("Lego Classic 1000 pieces", 850000, {"age": "4+", "brand": "Lego"}),
                ("Xe điều khiển từ xa", 250000, {"age": "6+", "battery": "Sạc"}),
                ("Bộ cờ vua quốc tế", 150000, {"material": "Nhựa cao cấp"}),
                ("Búp bê Barbie", 350000, {"brand": "Mattel"}),
                ("Đất nặn Play-Doh", 120000, {"pieces": "10 hộp"}),
                ("Robot biến hình Transformer", 450000, {"brand": "Hasbro"}),
                ("Súng nước đồ chơi", 80000, {"capacity": "500ml"}),
                ("Thú nhồi bông Gấu", 180000, {"size": "50cm"}),
                ("Đồ chơi bác sĩ", 150000, {"pieces": "15 chi tiết"}),
                ("Rubik 3x3", 50000, {"brand": "Gan"})
            ],
            "Văn phòng phẩm": [
                ("Bút bi Thiên Long (Hộp 20)", 60000, {"color": "Xanh"}),
                ("Sổ tay Moleskine", 250000, {"pages": "200", "size": "A5"}),
                ("Giấy A4 Double A", 75000, {"gsm": "80", "reams": "1"}),
                ("Hộp bút chì màu", 85000, {"colors": "24"}),
                ("File kẹp tài liệu", 25000, {"material": "Nhựa trong"}),
                ("Kéo văn phòng", 35000, {"size": "Vừa"}),
                ("Băng keo trong", 15000, {"width": "5cm"}),
                ("Giấy note vàng", 20000, {"pieces": "100 tờ"}),
                ("Bút dạ quang (Set 5)", 45000, {"colors": "Neon"}),
                ("Máy tính Casio fx-580", 650000, {"type": "Khoa học"})
            ],
            "Làm đẹp": [
                ("Son MAC Ruby Woo", 550000, {"brand": "MAC", "color": "Đỏ"}),
                ("Nước tẩy trang Bioderma", 350000, {"capacity": "500ml"}),
                ("Kem chống nắng La Roche-Posay", 420000, {"spf": "50+", "capacity": "50ml"}),
                ("Sữa rửa mặt Cetaphil", 280000, {"capacity": "500ml"}),
                ("Nước hoa hồng Mamonde", 250000, {"capacity": "250ml"}),
                ("Serum B5 The Ordinary", 220000, {"capacity": "30ml"}),
                ("Mặt nạ ngủ Laneige", 380000, {"capacity": "70ml"}),
                ("Phấn phủ Innisfree", 150000, {"weight": "5g"}),
                ("Dầu gội bưởi Cocoon", 180000, {"capacity": "300ml"}),
                ("Sữa tắm Love Beauty", 160000, {"capacity": "400ml"})
            ],
            "Sức khỏe": [
                ("Vitamin C DHC", 150000, {"brand": "DHC", "days": "60"}),
                ("Omega 3 Fish Oil", 250000, {"brand": "Kirkland", "capsules": "400"}),
                ("Sữa ong chúa Úc", 450000, {"brand": "Healthy Care", "capsules": "365"}),
                ("Máy đo huyết áp", 850000, {"brand": "Omron"}),
                ("Nhiệt kế hồng ngoại", 350000, {"brand": "Microlife"}),
                ("Khẩu trang y tế (Hộp 50)", 40000, {"layers": "4"}),
                ("Nước súc miệng Listerine", 120000, {"capacity": "750ml"}),
                ("Băng keo cá nhân", 20000, {"pieces": "100"}),
                ("Viên ngậm ho", 35000, {"brand": "Strepsils"}),
                ("Trà Atiso túi lọc", 55000, {"brand": "Vĩnh Tiến"})
            ],
            "Bách hóa online": [
                ("Mì tôm Hảo Hảo (Thùng)", 110000, {"brand": "Acecook", "pieces": "30"}),
                ("Sữa tươi Vinamilk 1L", 32000, {"brand": "Vinamilk", "sugar": "Ít đường"}),
                ("Dầu ăn Tường An 2L", 85000, {"brand": "Tường An"}),
                ("Nước mắm Nam Ngư", 45000, {"capacity": "750ml"}),
                ("Gạo ST25 5kg", 180000, {"brand": "A An"}),
                ("Cà phê Trung Nguyên Sáng tạo 1", 75000, {"weight": "340g"}),
                ("Nước giặt OMO Matic", 165000, {"capacity": "3.1kg"}),
                ("Giấy vệ sinh Watersilk", 55000, {"rolls": "10"}),
                ("Bột ngọt Ajinomoto", 60000, {"weight": "1kg"}),
                ("Nước giải khát Coca Cola", 10000, {"capacity": "330ml"})
            ],
            "Phụ kiện số": [
                ("Tai nghe AirPods Pro", 5500000, {"brand": "Apple", "type": "TWS"}),
                ("Cáp sạc Anker Type-C", 150000, {"brand": "Anker", "length": "1.2m"}),
                ("Sạc dự phòng Xiaomi 10000mAh", 350000, {"brand": "Xiaomi", "capacity": "10000mAh"}),
                ("Chuột không dây Logitech G304", 750000, {"brand": "Logitech", "type": "Gaming"}),
                ("Bàn phím cơ Akko", 1200000, {"brand": "Akko", "switch": "Red"}),
                ("Ốp lưng iPhone 15", 80000, {"brand": "Nillkin", "material": "Silicon"}),
                ("Kính cường lực iPad", 120000, {"brand": "Kingkong"}),
                ("Giá đỡ laptop nhôm", 250000, {"material": "Hợp kim nhôm"}),
                ("Hub chuyển đổi Type C 7in1", 450000, {"brand": "Baseus"}),
                ("Webcam HD 1080p", 550000, {"brand": "Razer"})
            ]
        }

        count_cat = 0
        count_prod = 0

        for cat_name, products in categories_dict.items():
            cat = Category.objects.create(name=cat_name, description=f"Danh mục {cat_name}")
            count_cat += 1
            for p_name, price, attrs in products:
                Product.objects.create(
                    name=p_name,
                    category=cat,
                    price=price,
                    stock=random.randint(20, 200),
                    attributes=attrs
                )
                count_prod += 1

        self.stdout.write(self.style.SUCCESS(f"Tạo thành công {count_cat} danh mục và {count_prod} sản phẩm."))
