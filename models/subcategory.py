class Subcategory:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def __repr__(self):
        return f"Subcategory(title={self.title}, link={self.link})"