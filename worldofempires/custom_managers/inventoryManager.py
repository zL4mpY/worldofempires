from worldofempires.custom_managers.itemManager import ItemManager

class Inventory():
    def __init__(self, entity, default_items=[]):
        self.entity = entity
        self.inventory = []
        self.inventory += default_items
    
    def get_item(self, item_id):
        for item in self.inventory:
            if item.id == item_id:
                return item
        return None
    
    def add_item(self, item_id, amount=1):
        for item in self.inventory:
            if item.id == item_id:
                item.add_amount(amount)
                return item_id
            
        self.inventory.append(ItemStack(item_id, amount))
        return item_id

    def remove_item(self, item_id, amount=1):
        for i, item in enumerate(self.inventory):
            if item.id == item_id:
                item.remove_amount(amount)
                if item == None: self.inventory.pop(i)
                return item
        return None

    def print_inventory(self):
        for item in self.inventory:
            print(f'{item.name}: {item.amount}')

class ItemStack():
    def __init__(self, item_id, amount):
        self.id = item_id
        self.amount = amount
        self.name = ItemManager().get_item_name_by_id(self.id)
        
    def remove_amount(self, amount):
        self.amount -= amount
        if amount <= 0:
            del self
            return 0
        return self.amount

    def add_amount(self, amount):
        self.amount += amount
        return self.amount