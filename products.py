from app import app, db
from db.models import Product

products = [
    {"name": "Стул деревянный", "description": "Удобный деревянный стул", "price": 1200.0, "stock": 20},
    {"name": "Стол письменный", "description": "Стол для работы и учебы", "price": 4500.0, "stock": 10},
    {"name": "Кресло офисное", "description": "Комфортное кресло для офиса", "price": 6000.0, "stock": 15},
    {"name": "Диван угловой", "description": "Большой угловой диван", "price": 15000.0, "stock": 5},
    {"name": "Кровать двуспальная", "description": "Удобная двуспальная кровать", "price": 18000.0, "stock": 8},
    {"name": "Шкаф для одежды", "description": "Шкаф с двумя дверцами", "price": 8000.0, "stock": 12},
    {"name": "Комод", "description": "Комод с пятью ящиками", "price": 5000.0, "stock": 10},
    {"name": "Тумбочка", "description": "Тумбочка прикроватная", "price": 2000.0, "stock": 30},
    {"name": "Полка навесная", "description": "Деревянная полка для книг", "price": 1500.0, "stock": 25},
    {"name": "Стул пластиковый", "description": "Простой пластиковый стул", "price": 800.0, "stock": 50},
    {"name": "Кресло кожаное", "description": "Кожаное кресло премиум класса", "price": 12000.0, "stock": 7},
    {"name": "Диван раскладной", "description": "Диван с механизмом раскладывания", "price": 20000.0, "stock": 4},
    {"name": "Кухонный стол", "description": "Стол для кухни на 4 персоны", "price": 7000.0, "stock": 10},
    {"name": "Кухонный стул", "description": "Компактный кухонный стул", "price": 1100.0, "stock": 35},
    {"name": "Журнальный столик", "description": "Столик для гостиной", "price": 4000.0, "stock": 20},
    {"name": "Шкаф угловой", "description": "Угловой шкаф для хранения вещей", "price": 14000.0, "stock": 6},
    {"name": "Пуфик", "description": "Мягкий пуфик для отдыха", "price": 2500.0, "stock": 18},
    {"name": "Книжный шкаф", "description": "Шкаф для книг", "price": 10000.0, "stock": 9},
    {"name": "Зеркало настенное", "description": "Зеркало с деревянной рамой", "price": 3500.0, "stock": 15},
    {"name": "Тумба под ТВ", "description": "Тумба с отделениями для техники", "price": 5500.0, "stock": 12},
    {"name": "Детская кровать", "description": "Кровать для ребёнка с бортиками", "price": 9000.0, "stock": 10},
    {"name": "Компьютерный стол", "description": "Стол с подставкой для ПК", "price": 6000.0, "stock": 8},
    {"name": "Шкаф-купе", "description": "Шкаф с раздвижными дверцами", "price": 20000.0, "stock": 5},
    {"name": "Обеденный стол", "description": "Большой обеденный стол на 6 персон", "price": 12000.0, "stock": 7},
    {"name": "Кухонный уголок", "description": "Мягкий уголок для кухни", "price": 15000.0, "stock": 4},
    {"name": "Кресло-груша", "description": "Мягкое кресло-груша", "price": 3000.0, "stock": 20},
    {"name": "Матрас ортопедический", "description": "Матрас с ортопедическим эффектом", "price": 10000.0, "stock": 15},
    {"name": "Шезлонг", "description": "Лежак для отдыха", "price": 7000.0, "stock": 10},
    {"name": "Кухонный гарнитур", "description": "Комплект мебели для кухни", "price": 50000.0, "stock": 3},
]

with app.app_context():
    for product in products:
        existing_product = Product.query.filter_by(name=product["name"]).first()
        if not existing_product:
            new_product = Product(
                name=product["name"],
                description=product["description"],
                price=product["price"],
                stock=product["stock"]
            )
            db.session.add(new_product)
    db.session.commit()
