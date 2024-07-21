class FoodItem:
    def __init__(self, name, food_id, food_desc, has_kilo_price, has_piece_price, price_per_kilo, deleted_price_per_kilo, deleted_main_price, main_price):
        self.name = name
        self.food_id = food_id
        self.food_desc = food_desc
        self.has_kilo_price = has_kilo_price
        self.has_piece_price = has_piece_price
        self.price_per_kilo = price_per_kilo
        self.deleted_price_per_kilo = deleted_price_per_kilo
        self.deleted_main_price = deleted_main_price
        self.main_price = main_price

    def add_food_item(self, food_item):
        self.food_item.append(food_item)

    def __repr__(self):
        return f"FoodItem(name={self.name}, deleted_price_per_kilo={self.deleted_price_per_kilo}, price_per_kilo={self.price_per_kilo}, deleted_main_price={self.deleted_main_price}, main_price={self.main_price})"