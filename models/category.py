class Category:
    def __init__(self, title):
        self.title = title
        self.subcategories = []

    def add_subcategory(self, subcategory):
        self.subcategories.append(subcategory)

    def __repr__(self):
        return f"Category(title={self.title}, subcategories={self.subcategories})"