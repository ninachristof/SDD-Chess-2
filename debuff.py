class debuff():
    description = ""
    id = 0

    def __init__(self,new_description,new_id):
        self.description = new_description
        self.id = new_id

    def get_description(self):
        return self.description
    
    def get_id(self):
        return self.id

def filter_debuff(moves,id):
    if (id == 1):
        print("Euclidean Distance at most 6")
    if (id == 2):
        print("Can't move more than 2 rows or columns from current position")
    if (id == 3):
        print("Can only move every other turn")