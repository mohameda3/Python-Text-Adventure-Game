class Player:

    def __init__(self, x, y, inventory=[]):
        '''
        Creates a new Player.
        :param x: x-coordinate of position on map
        :param y: y-coordinate of position on map
        :return:

        This is a suggested starter class for Player.
        You may add new parameters / attributes / methods to this class as you see fit.
        Consider every method in this Player class as a "suggested method":
                -- Suggested Method (You may remove/modify/rename these as you like) --
        '''
        self.x = x
        self.y = y
        self.inventory = inventory
        self.victory = False
        self.loss = False

    def move(self, dx, dy):
        '''
        Given integers dx and dy, move player to new location (self.x + dx, self.y + dy)
        :param dx: int value representing the change in the x value
        :param dy: int value represeenting the change in the y value.
        :return:
        '''
        self.x = self.x + dx
        self.y = self.y + dy



    def move_north(self):
        '''These integer directions are based on how the map must be stored
        in our nested list World.map For north dx = 0 and dy = -1'''
        self.move(0, -1)

    def move_south(self):
        '''These integer directions are based on how the map must be stored
        in our nested list World.map For south dx = 0 and dy = 1'''
        self.move(0, 1)

    def move_east(self):
        '''These integer directions are based on how the map must be stored
        in our nested list World.map For east dx = 1 and dy = 0'''
        self.move(1, 0)

    def move_west(self):
        '''These integer directions are based on how the map must be stored
        in our nested list World.map For west dx = -1 and dy = 0'''
        self.move(-1, 0)

    def add_item(self, item, location):
        '''
        This function appends an item to player's inventory and removes it from the location.
        :param item: The item the is being taken from the location.
        :param location: The location where the item currently is.
        :return: return inventory with the appended item.
        '''

        location.items.remove(item)
        return self.inventory.append(item)

    def remove_and_drop_item(self, item, location):
        '''
        This function removes an item from player's inventory and appends it to the location.
        :param item: The item that is being removed from the inventory
        :param location: The location that the item is being appended/dropped to.
        :return: return inventory without the item that is removed.
        '''
        location.items.append(item)
        return self.inventory.remove(item)

    def swap_item(self,item_swap, item_swap_for,location):
        '''
        This function swaps an item from the player's inventory for an item that is in the current location.
        :param item_swap: the item that is being traded from the players inventory
        :param item_swap_for: the item that is being traded for in the location
        :param location: the location of the swap.
        :return:
        '''
        self.inventory.remove(item_swap)
        location.items.remove(item_swap_for)
        location.items.append(item_swap)
        self.inventory.append(item_swap_for)

    def get_inventory(self):
        '''
        Return inventory.
        '''
        return self.inventory