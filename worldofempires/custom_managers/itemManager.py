from engine import in_dict

items = {1: "Wood",
         2: "Stone",
         3: "Iron ore",
         4: "Silver ore",
         5: "Gold ore"}


class ItemManager():
    def get_item_name_by_id(self, id: int) -> str:
        if in_dict(id, items):
            return items[id]
        return None
    
    def get_item_id_by_name(self, name: str) -> int:
        name = name.replace(' ', '').lower()
        
        for key, value in items.items():
            if value.replace(' ', '').lower() == name:
                return key
        return None