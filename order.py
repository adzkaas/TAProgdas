
class Item:
    def __init__(self, name, price, image_path, description):
        self._name = name
        self._price = price
        self._image_path = image_path
        self._description = description

    # Getter dan Setter untuk nama
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    # Getter dan Setter untuk harga
    def get_price(self):
        return self._price
    
    def set_price(self, price):
        self._price = price

    # Getter dan Setter untuk gambar
    def get_image(self):
        return self._image_path
    
    def set_image(self, image_path):
        self._image_path = image_path

    # Getter untuk deskripsi
    def get_description(self):
        return self._description


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self):
        if self.items:
            return self.items.pop()
        return None

    def get_items(self):
        return self.items

    def get_total(self):
        return sum(item.get_price() for item in self.items)

    def clear_cart(self):
        self.items.clear()
