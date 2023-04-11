class Item:
    def __init__(self, name, price, info, quantity):
        self.name = name
        self.price = price
        self.info = info
        self.quantity = quantity

    def __str__(self):
        return f'{self.name}|{self.info}'
    def __repr__(self):
        return self.__str__()

class Inventory:
    def __init__(self):
        self.__item_list = [] # blank list
        self.__index = -1 # -1 because __next__ increases by 1 /before/ executing any code

    def add_item(self,name,price,info,quantity):
        current_item = Item(name,price,info,quantity)
        self.__item_list.append(current_item)

    def __iter__(self): # Declare that class is iterable
        return self
     
    def __next__(self): # When iterating to next item in list
        self.__index += 1 # increase index counter by 1
        if self.__index == len(self.__item_list):
            self.__index = -1 # reset index back to -1
            raise StopIteration # Lets python know to stop iterating
        else:
            # return the value @ our given index
            return self.__item_list[self.__index]
        
    def get_item_list(self):
        return self.__item_list
            
        
        