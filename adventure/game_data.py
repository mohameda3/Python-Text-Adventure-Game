import os
class Location:

    def __init__(self, index, score, short_desc, long_desc, items, x, y, accessible, visited=False):
        '''
        Creates a new location with these parameters below.
        :param index: an unique int that represents the position in the map of the location.
        :param score: an int that represents the score for visiting the location for the first time.
        :param short_desc: a string representing the short description of the location.
        :param long_desc: a string representing the long description of the location.
        :param items: a list of item objects for the location.
        :param x: an int x coordinate of the location in the map
        :param y: an int y coordinate of the location in the map
        :param accessible: an int representing the type of accessibility for the location.
        :param visited: a bool representing whether the location has been visited or not.
        '''
        self.index = index
        self.score = score
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.items = items
        self.x = x
        self.y = y
        self.accessible = accessible
        self.visited = visited

    def get_index(self):
        '''Return int index number of location.'''
        return int(self.index)

    def get_score(self):
        '''Return int score for visiting location for the first time.'''
        return self.score

    def get_brief_description(self):
        '''Return str brief description of location.'''
        return self.short_desc

    def get_full_description(self):
        '''Return str long description of location.'''
        return self.long_desc

    def get_items(self):
        '''Return items for each location as a list of item instances.'''
        return self.items

    def get_x(self):
        '''Return int x coordinate of the location on the map.'''
        return int(self.x)

    def get_y(self):
        '''Return int y coordinate of the location on the map.'''
        return int(self.x)

    def get_visited(self):
        '''Return bool value on whether the location has been visited or not. Initially is false.'''
        return self.visited

    def get_accessible(self):
        '''
        Return int value which represents the type of accessibility for each location/
        0 - You cannot drop/pick up in this location.
        1 - No restrictions.
        2 - In order to move forward, you must complete an event.
        3 - You cannot leave/drop/pick up in this location. You currently have everything you need to write the exam.
        '''
        return self.accessible

    def available_actions(self):
        '''
        Return the available actions for this location as a list.
        Initially has all the cardinal directions and pick up/swap/enter/write where appropriate.
        Drop will be added as an action where appropriate in adventure.
        '''
        available_actions = ["Go North", "Go East", "Go South", "Go West"]
        if len(self.items) > 0:
            for i in self.items:
                if self.accessible == 1:
                    available_actions.append("Pick up " + i.name)
                elif self.accessible == 0:
                    available_actions.append("Swap Sheets")
        if self.accessible == 2:
            available_actions.append("Enter the Exam")
        elif self.accessible == 3:
            available_actions.append("Write the Exam")
        elif self.accessible == 4:
            available_actions.append("Confront man")
        return available_actions

class Item:

    def __init__ (self, name, start, target, target_points, weight, inspect):
        '''
        Create item object with attributes filled by the parameters below:
        :param name: A str value that represents the item's name.
        :param start: A int value that represents the starting location of the item.
        :param target: A int value that represents the target location of the item.
        :param target_points: A int value that represents the score the player gets for dropping the item at its target.
        :param weight: A int value that represents how much an item weighs.
        :param inspect: A str value that gives greater detail on the item.
        '''

        self.name = name
        self.start = start
        self.target = target
        self.target_points = target_points
        self.weight = weight
        self.inspect = inspect

    def get_starting_location(self):
        '''Return int location where item is first found.'''
        return self.start

    def get_name(self):
        '''Return the str name of the item.'''
        return self.name

    def get_target_location(self):
        '''Return item's int target location where it should be deposited.'''
        return self.target

    def get_target_points(self):
        '''Return int points awarded for depositing the item in its target location.'''
        return self.target_points

    def get_weight(self):
        '''Return int weight value of item.'''
        return self.weight

    def get_inspect(self):
        '''Return str description of the item.'''
        return self.inspect

class World:

    def __init__(self, mapdata, locdata, itemdata):
        '''
        Creates a new world using the information from locations.txt (for location info),
        items.txt(for item info), and map.txt(for map info).
        :param mapdata: A string that gives the name of the textfile where map data is located. Map must be a nested list.
        :param locdata: A string that gives the name of the textfile where location data is located.
        :param itemdata: A string that gives the name of the textfile where item data is located.
        :return:
        '''
        self.map = self.load_map(mapdata)
        self.items = self.load_items(itemdata)
        self.locations = self.load_locations(locdata, self.items)

    def load_map(self, filename):
        '''
        Store map from filename (map.txt) in the variable "self.map" as a nested list of integers.
        map:    1 2 5
                3 -1 4
        becomes [[1,2,5], [3,-1,4]]
        :param filename: string that gives name of text file in which map data is located
        :return: returns a nested list of "integers" representing map of game world as specified above
        '''

        map = []
        if os.path.exists(filename):
            f = open(filename, "r")
            for line in f:
                row = line.strip("\n").split(" ")
                row_int = []
                for string in row:
                    row_int.append(int(string))

                map.append(row_int)
            return map
        else:
            print("Error: Unable to load map")
            print(".....Map file not found......")
            quit()

    def load_locations(self, filename, items):
        '''
        Store all locations from filename (locations.txt) into the variable "self.locations"
        by reading the file, assigning attributes to the each location object based on the contents
        of the file as well as the item list.
        :param filename: string that gives name of text file in which location data is located
        :param items: list of item objects that will be added to their appropriate locations.
        :return: return a list of location objects, each object representing a single location in the map.
        '''

        locations = []
        if os.path.exists(filename):
            f = open(filename, "r")

            location_blocks = f.read().split("END\n\n")

            for location in location_blocks:
                lines = location.split("\n")

                index = int(lines[0].strip("LOCATION "))
                score = int(lines[1])
                accessible = int(lines[2])
                short_desc = lines[3]
                long_desc = "\n".join(lines[4:])
                long_desc = long_desc.strip("END")
                visited = False

                '''
                To get the items from all of the map, and put them in their location
                '''
                temp_items = []
                for i in items:
                    if i.start == index:
                        temp_items.append(i)

                for column in range(len(self.map)):
                    for row in range(len(self.map[column])):
                        if self.map[column][row] == index:
                            x = row
                            y = column

                            new_loc = Location(index, score, short_desc, long_desc, temp_items, x, y, accessible, visited)
                            locations.append(new_loc)
            f.close()
            return locations
        else:
            print("Error: Unable to load locations")
            print(".....Locations file not found......")
            quit()

    def load_items(self, filename):
        '''
        Store all items from filename (items.txt) into the variable "self.items" which is a list of item objects.
        Each object has attributes based on the contents of the file.
        :param filename: string that gives name of text file in which item data is located.
        :return: return a list of item objects, each object representing a single item in a location.
        '''

        items = []
        if os.path.exists(filename):
            f = open(filename, "r")

            item_blocks = f.read().split("\n\n")

            for item in item_blocks:
                lines = item.split("\n")
                name = lines[0]
                start = int(lines[1])
                target = int(lines[2])
                target_points = int(lines[3])
                weight = int(lines[4])
                inspect = lines[5]

                new_item = Item(name, start, target, target_points, weight, inspect)
                items.append(new_item)
            f.close()
            return items
        else:
            print("Error: Unable to load items")
            print(".....Items file not found......")
            quit()

    def get_location(self, x, y):
        '''Check if location exists at location (x,y) in world map.
        Return Location object associated with this location if it does. Else, return None.
        Remember, locations represented by the number -1 on the map should return None.
        :param x: integer x representing x-coordinate of world map
        :param y: integer y representing y-coordinate of world map
        :return: Return Location object associated with this location if it does. Else, return None.
        Example:
        map = 1 2 5
              3 -1 4

        get_location(5,0) would return None
        get_location(0,0) would return location with index 1
        get_location(2,1) would return location with index 4
        '''

        for loc in self.locations:
            if (x == loc.x and y == loc.y) and loc.index != -1:
                return loc
        return None
