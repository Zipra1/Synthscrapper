from inventory import Inventory

database = Inventory()
database.add_item('Pizza',3,'slice of pizza',20)
database.add_item('Pop',1,'fizzy',100)
database.add_item('Dip',0.5,'almost liquid',3)

for item in database: ## This is possible because Inventory was declared to be iterable.
    print(item)
print(database.get_item_list())