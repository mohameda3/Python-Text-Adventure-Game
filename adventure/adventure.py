from game_data import World, Item, Location
from player import Player

'''
Sets all values equal to their initial values.
ie. Score is zero before the game.
ie. Carry weight is zero as nothing has been picked up.
'''
score = 0
moves = -1
carry_weight = 0
puzzle_attempts = 0
entry_attempts = 2
max_score = 190
max_moves = 35
max_carry_weight = 10
player_inventory_names = []
droppable_items = []


def check_move(temp_move):
    '''
    Checks if the move chosen would take PLAYER outside of the map. If so it returns false and prints a statement
    letting PLAYER know that he should not go there.
    :param temp_move: Temp move is a temporary cardinal move.
    :return: returns True if that move is possible, else returns false.
    '''

    if temp_move != -1 and temp_move is not None:
        return True
    else:
        print("Leaving the campus would not be wise. You decide to not leave.")
        return False

if __name__ == "__main__":
    WORLD = World("map.txt", "locations.txt", "items.txt")
    PLAYER = Player(1, 1)  # starting location of the player.

    menu = ["Look", "Inventory", "Score", "Quit", "Back", "Carry Weight"]

    '''
    Sets the initializes the values for performing actions loop as well as
    [menu] loop. Starts the loop that exits only when the Player has lost or won.
    Score is only added if the player visits a new location here. Moves only increase
    when a player changes location, so commands like drop/pick up will not increase the move count.
    If the player's moves is equal to the maximum number of moves then the player loses. We also find
    every possible cardinal move for that location ie. temp_north value.
    '''
    performing_actions = True
    in_menu = False
    while not PLAYER.victory and not PLAYER.loss:
        location = WORLD.get_location(PLAYER.x, PLAYER.y)

        if location.visited is False:
            print(location.long_desc)
            location.visited = True
            score += location.score
        else:
            print(location.short_desc)
        moves += 1
        print("Moves:", moves, "out of", max_moves, "\nYour score is: ", score)

        if moves > max_moves:
            PLAYER.loss = True

        temp_north = WORLD.get_location(PLAYER.x, PLAYER.y-1)
        temp_east = WORLD.get_location(PLAYER.x + 1, PLAYER.y)
        temp_south = WORLD.get_location(PLAYER.x, PLAYER.y + 1)
        temp_west = WORLD.get_location(PLAYER.x-1, PLAYER.y)
        performing_actions = True

        '''
        First this loop prints out all the available commands for this location
        depending on the users inventory. This loop checks the accessibility levels
        of each location and prints an available response for each command.
        i.e. if the player attempts to pick up an item but misspells that item it will notify them.
        Also if a plauer cannot pick up an item due to going over the carry weight, the program
        will recognize this and let the player know this problem.Certain commands like "swap sheets",
        "enter the exam","write the exam", and "confront man" are ocation specific and may require
        you to possess an item in your inventory in order to continue.These commands will notifiy you
        if you are missing something that is required. This loop will only activate when the player
        requests to visit the other menu screen, and vice versa.
        '''

        while performing_actions:
            print("What to do? \n\n[menu]")
            for action in location.available_actions():
                print(action)
            if len(droppable_items) > 0:
                for item in droppable_items:
                    print("Drop " + item)

            choice = input("\nEnter action: ").lower()

            if location.accessible == 3 and choice.startswith("go "):
                print("You may not leave this location, the exam is starting soon.\nPlease write the exam.")

            elif choice == "go north" and check_move(temp_north):
                if location.accessible != 3:
                    PLAYER.move_north()
                    break
                else:
                    print("You cannot leave in that direction at this time.")

            elif choice == "go south" and check_move(temp_south):
                if location.accessible == 2:
                    print("You must pass the security check to enter the exam.")
                elif location.accessible == 3:
                    print("You cannot leave in that direction at this time.")
                else:
                    PLAYER.move_south()
                    break

            elif choice == "go east" and check_move(temp_east):
                if location.accessible != 3:
                    PLAYER.move_east()
                    break
                else:
                    print("You cannot leave in that direction at this time.")

            elif choice == "go west" and check_move(temp_west):
                if location.accessible != 3:
                    PLAYER.move_west()
                    break
                else:
                    print("You cannot leave in that direction at this time.")

            elif choice.startswith("pick up ") and len(location.items) > 0:
                if location.accessible == 1:
                        not_picked_up = True
                        for item in location.items:
                            if choice[8:] == item.name.lower() and location.accessible:
                                not_picked_up = False
                                if (carry_weight + item.weight) <= max_carry_weight :
                                    Player.add_item(PLAYER, item, location)
                                    menu.append("Inspect " + item.name)
                                    droppable_items.append(item.name)
                                    player_inventory_names.append(item.name)
                                    carry_weight += item.weight
                                    print("You picked up {0}.".format(item.name))
                                else:
                                    print("Carrying another item would be too heavy, drop an item first.")
                        if not_picked_up:
                            print("Pick up Error: Failed to pick up please spell correctly.")
                else:
                    print("You cannot pick up items in this location. Please choose another command.")

            elif choice.startswith("drop ") and len(PLAYER.inventory) > 0:
                if location.accessible == 1:
                        not_dropped = True
                        for item in PLAYER.inventory:
                            if choice[5:] == item.name.lower() and location.accessible == 1 or location == 2:
                                Player.remove_and_drop_item(PLAYER, item, location)
                                menu.remove("Inspect " + item.name)
                                droppable_items.remove(item.name)
                                player_inventory_names.remove(item.name)
                                carry_weight -= item.weight
                                not_dropped = False
                                if item.target == location.index:
                                    score += item.target_points
                                    location.items.remove(item)
                                print("You dropped {0} from your inventory.".format(item.name))
                        if not_dropped:
                            print("Drop Error: Failed to drop please spell correctly.")
                else:
                    print("You cannot drop items in this location. Please choose another command.")

            elif choice.startswith("swap ") and len(PLAYER.inventory) > 0:
                    if location.accessible == 0 and choice == "swap sheets":
                        swap_not_done = True
                        for swapped_item in PLAYER.inventory:
                            if swapped_item.name == "Cheat Sheet" or swapped_item.name == "Exam Answer Sheet":
                                for swapped_for in location.items:
                                    if (swapped_for.name == "Cheat Sheet" or swapped_for.name == "Exam Answer Sheet") and swap_not_done:
                                        Player.swap_item(PLAYER, swapped_item, swapped_for, location)
                                        player_inventory_names.remove(swapped_item.name)
                                        player_inventory_names.append(swapped_for.name)
                                        droppable_items.remove(swapped_item.name)
                                        droppable_items.append(swapped_for.name)
                                        menu.remove("Inspect " + swapped_item.name)
                                        menu.append("Inspect " + swapped_for.name)
                                        swap_not_done = False
                                        print("You swapped your {0} for {1}.".format(swapped_item.name, swapped_for.name))
                                        print("No one will suspect a thing.")
                        if swap_not_done:
                            print("You do not have the correct item to swap.")
                    else:
                        print("Swap Error: Please spell correctly.")

            elif choice == "enter the exam" and location.accessible == 2:
                print("Guard: Do you have what it takes to enter the exam?")
                print("Input 1 for yes. Anything else for no.")
                decision = input("\nChoose:\n")
                if decision == "1":
                    print("We'll see how ready you really are hotshot.")
                    if "Knife" in player_inventory_names:
                        print("What is this knife doing in your bag, you hooligan!\nYou're not writing this exam!")
                        performing_actions = False
                        PLAYER.loss = True
                    elif "Cheat Sheet" and "T-card" and "Lucky Pen" in player_inventory_names:
                        print("Well it looks like you have everything you need. Go fail that exam hotshot.")
                        PLAYER.move_south()
                        performing_actions = False
                    elif entry_attempts == 0:
                        print("You've pulled my last nerve by coming here unprepared again.")
                        print("You're not writing this exam kid. Good luck retaking this course next year.")
                        PLAYER.loss = True
                        performing_actions = False
                    else:
                        print("Well, looks like your unprepared. Watch what happens if you come back here again.")
                        entry_attempts -= 1
                else:
                    print("Well then what are you wasting my time here for? Get outta here.")

            elif choice == "write the exam" and location.accessible == 3:
                if "Cheat Sheet" in player_inventory_names and "T-card" in player_inventory_names and "Lucky Pen" in player_inventory_names:
                    for item in PLAYER.inventory:
                        if item.target == location.index:
                            score += item.target_points
                    PLAYER.victory = True
                    performing_actions = False

                elif "Exam Answer Sheet" in player_inventory_names and "T-card" in player_inventory_names and "Lucky Pen" in player_inventory_names:
                    for item in PLAYER.inventory:
                        if item.target == location.index:
                            score += item.target_points
                    performing_actions = False
                    PLAYER.victory = True

            elif choice == "confront man" and location.accessible == 4:
                print("You approach the man wearing a dark overcoat...\nHe turns around and you see the face of a clown.")
                print("The man begins to speak.")
                if puzzle_attempts == 0:
                    puzzle_answer = input("What building has the most stories?\n").lower()
                    if "library" in puzzle_answer:
                        print("Correctamundo")
                        trade = input("Do you wanna trade a knife for a super secret special item?\nType 1 for yes.\n")
                        if trade == "1":
                            if "Knife" in player_inventory_names:
                                print("Here take my golden rabbits foot. It weighs ZERO pounds so it wont hurt your back.")
                                for get_item in location.items:
                                    if get_item.name == "Golden Rabbit's Foot":
                                        for give_item in PLAYER.inventory:
                                            if give_item.name == "Knife":
                                                Player.swap_item(PLAYER, give_item, get_item, location)
                                                player_inventory_names.remove(give_item.name)
                                                player_inventory_names.append(get_item.name)
                                                droppable_items.remove(give_item.name)
                                                droppable_items.append(get_item.name)
                                                carry_weight -= give_item.weight
                                                menu.append("Inspect " + get_item.name)
                                                menu.remove("Inspect " + give_item.name)
                                                puzzle_attempts = 2
                                                print("Good trading with ya'.")
                            else:
                                print("It seems you don't have a knife in your inventory. Come back when you smarten up.")
                                puzzle_attempts += 1
                        else:
                            print("Well, come back later if you want.")
                            puzzle_attempts += 1
                    else:
                        print("You got it wrong, you loser. Come back again some time.")
                        puzzle_attempts += 1
                elif puzzle_attempts == 1:
                    puzzle_answer2 = input("What do you get when you multiply all the numbers on a telephone pad?\n").lower()
                    if puzzle_answer2 == "0":
                        print("Correctamundo")
                        trade = input("Do you wanna trade a knife for a super secret special item?\nType 1 for yes.")
                        if trade == "1":
                            if "Knife" in player_inventory_names:
                                print("Here take my golden rabbits foot. It weighs ZERO pounds so it wont hurt your back.")
                                for get_item in location.items:
                                    if get_item.name == "Golden Rabbit's Foot":
                                        trade_foot = get_item
                                        for give_item in PLAYER.inventory:
                                            if give_item.name == "Knife":
                                                trade_knife = give_item
                                                Player.swap_item(PLAYER, trade_knife, trade_foot, location)
                                                player_inventory_names.remove(give_item.name)
                                                player_inventory_names.append(get_item.name)
                                                droppable_items.remove(give_item.name)
                                                droppable_items.append(get_item.name)
                                                carry_weight -= give_item.weight
                                                menu.append("Inspect " + get_item.name)
                                                menu.remove("Inspect " + give_item.name)
                                                puzzle_attempts = 2
                                                print("Good trading with ya'.")

                            else:
                                print("It seems you don't have a knife in your inventory. Come back when you smarten up.")
                                print("Jokes you can't cause that was your last attempt. MWhahahhaaaaa.....")
                                puzzle_attempts += 1
                        else:
                            print("Well, come back later if you want...Sorry you can't lololol.")
                            puzzle_attempts += 1
                    else:
                        print("Wow....For a university student you sure can't multiply.")
                        puzzle_attempts += 1
                else:
                    print("Were done dealing right now kiddo. Beat it.")
                    puzzle_attempts += 1

            elif choice == "[menu]":
                performing_actions = False
                in_menu = True
                '''
                Handles all code for submenu if [menu] is selected
                '''
            else:
                print("Invalid Input")

            '''
            This menu is only activated when the player is in the performing actions menu, and enters
            the [menu] command. The back command here turns of this menu loop and activates the performing
            actions loop. The inspect command gives more information about an item and changes along with
            the inventory. Score represents how much points you have recieved and carry weight is the sum of
            the weights of every item you are carrying. Quit command terminates the game.
            '''

            while in_menu:
                print("Menu Options: \n")
                for option in menu:
                    print(option)
                choice = input("\nChoose action: ").lower()
                if choice == "quit":
                    print("Program Terminated")
                    exit()
                elif choice == "look":
                    print(location.long_desc)
                elif choice == "score":
                    print("Your current score is ", score)
                elif choice == "inventory":
                    print("\nInventory: ", player_inventory_names)
                elif choice == "back":
                    in_menu = False
                    performing_actions = True
                elif choice.startswith("inspect "):
                    error = True
                    for item in PLAYER.inventory:
                        if choice[8:] == item.name.lower():
                            print(item.inspect)
                            error = False
                    if error:
                        print("Inspect error: Please spell correctly.")
                elif choice == "carry weight":
                    print("Your carry weight is {0} out of {1}".format(carry_weight, max_carry_weight))
                else:
                    print("Invalid Input.")

    '''
    This if statement executes when the game ends letting the user whether they won, and if
    appropriate how well they did compared to the maximum score that you can get. There score
    will be converted into a percentage, and that percentage represents the player's mark on
    the exam. Player's are encouraged to continue playing until they get 100% on their exams.
    '''

    if PLAYER.victory:
        print("Congrats You've won!\nYour score is {0} out of {1}".format(score, max_score))
        print("Your mark on the exam was", round((score/max_score)*100, 4), "%")
    else:
        print("You lost.\nBetter luck next time.")

