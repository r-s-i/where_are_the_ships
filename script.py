from ast import Break
import random
import time
import os
clear = lambda: os.system('clear')


class Game:
    def __init__(self):
        self.map = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        self.boats_horizontal = {2: ["<", ">"], 3: ["<", "#", ">"], 4: ["<", "#", "#", ">"]}
        self.boats_vertical = {2: ["ʌ", "v"], 3: ["ʌ", "#", "v"], 4: ["ʌ", "#", "#", "v"]}
        self.shell_reserves = 40
        self.sea_unhit = "~"
        self.sea_hit = "o"
        self.ship_hit = "x"
        self.boats_part = 0
        self.is_game_over = False

        # Counts the number of boats part:
        def count_dict_list_parts(self, dict):
            for key in dict:
                for part in dict[key]:
                    self.boats_part += 1
        # Vertical boats:
        count_dict_list_parts(self, self.boats_horizontal)
        # Horizontal boats:
        count_dict_list_parts(self, self.boats_vertical)

        # Populate map with 7 cells each:
        for key in self.map:
            for i in range(7):
                self.map[key].append(self.sea_unhit)

        # Populate random rows with one ship each:
        possible_row = [*range(7)]
        for key in self.boats_horizontal:
            random_x_offset = random.randint(0, 6-len(self.boats_horizontal[key]))
            line = random.choice(possible_row)
            possible_row.remove(line)
            
            for i in range(len(self.boats_horizontal[key])):
                self.map[line][i+random_x_offset] = self.boats_horizontal[key][i]
        
        # Populate random columns with one ship each:
        possible_columns = [*range(7)]
        for key in self.boats_vertical:
                not_fitted = True
                while (not_fitted):
                    column = random.choice(possible_columns)
                    # Picks a vacant part of column:
                    coloumn_cells = []
                    for i in range(7):
                        coloumn_cells.append(self.map[i][column])
                    
                    # Where does the boat fit:
                    num_to_fit = 0
                    cell_num = 1
                    for cell in coloumn_cells:
                        if (cell == self.sea_unhit):
                            num_to_fit += 1
                        else:
                            num_to_fit = 0
                        # When it has found enough cells to place the boat:
                        if (num_to_fit == len(self.boats_vertical[key])):                        
                            break
                        cell_num += 1
                    # Places the boat where it fits:
                    if (num_to_fit == len(self.boats_vertical[key])):
                        for i in range(num_to_fit):
                            self.map[(cell_num-num_to_fit)+i][column] = self.boats_vertical[key][i]
                        not_fitted = False                      

    def round(self, user_input):
        clear()
        # If game is over, don't do anything:
        if (self.is_game_over):
            print("The game is over, type exit(e) to quit, return(r) to go to the start screen.")
            return
        user_input_list = list(user_input.split(","))
        try:
            if (self.map[int(user_input_list[0])-1][int(user_input_list[1])-1] != self.sea_unhit 
            and self.map[int(user_input_list[0])-1][int(user_input_list[1])-1] != self.ship_hit
            and self.map[int(user_input_list[0])-1][int(user_input_list[1])-1] != self.sea_hit):
                print("You hit something!")
                self.map[int(user_input_list[0])-1][int(user_input_list[1])-1] = self.ship_hit
            elif (self.map[int(user_input_list[0])-1][int(user_input_list[1])-1] == self.ship_hit
            or self.map[int(user_input_list[0])-1][int(user_input_list[1])-1] == self.sea_hit):
                print("You have already fired at this cell...") 
            else:
                print("You missed!")
                self.map[int(user_input_list[0])-1][int(user_input_list[1])-1] = self.sea_hit
            self.shell_reserves -= 1
            if (self.shell_reserves > 0):
                print(f"You have {self.shell_reserves} shells left.")
        except:
            print("I'm sorry, I don't understand. Try again.")
  
        # Checks to if the player has won:
        count = 0
        for line in self.map:
            for cell in self.map[line]:
                if (cell == self.ship_hit):
                    count += 1
        if (count >= self.boats_part):
            print("You destroyed all the ships. Congratulations, thousands are dead. )=")
            self.is_game_over = True
        
        # Checks to see if player has lost:
        if (self.shell_reserves <= 0 and not self.is_game_over):
            self.is_game_over = True
            print("You ran out of shells. Game over.")
        
        # If game is not over:
        # Prints out the hidden map:
        if (self.shell_reserves > 0):
            self.print_hidden_map()
        # If game is over:
        else:
            for key in self.map:
                line_str = " "
                print(line_str.join(self.map[key]))

    def print_hidden_map(self):
        for key in self.map:
            new_line = []
            # Shows hits and misses:
            for char in self.map[key]:
                if (char == self.sea_hit):
                    new_line.append(char) 
                elif (char == self.ship_hit):
                    new_line.append(char)
                else:
                    new_line.append(self.sea_unhit)         
            new_line_str = " "
            print(new_line_str.join(new_line))  

def start_screen():                  
    # Asks the player if he wants to start the game, 
    # read the instructions, or end the game.
    print("Type play (p) to 'play' the game, 'how' (h) for instructions, and exit(e) to quit.")
    user_input = input()
    user_input = user_input.lower()

    # If he wants to start the game:
    if (user_input == "play" or user_input == "p"):
        new_game = Game()

        print("Please select a cell (e.g.: '3,6')")
        new_game.print_hidden_map()

        while (True):
            user_input = input()
            user_input = user_input.lower()
            # If user want's to exit while playing:
            if (user_input == "exit" or user_input == "e"):
                print("Goodbye...")
                time.sleep(1)
                exit()
            # If user want's to return to start screen:
            if (user_input == "return" or user_input == "r"):
                start_screen()
            new_game.round(user_input)

    # If he wants to read the instructions:          
    elif (user_input == "how" or user_input == "h"):
        print("Press any key to return to the start screen.")
        print("Write 'return' or 'r' to return to the start screen while playing.")
        print()
        print("Your job is to destroy hidden ships.")
        print("You play by selecting cells in a 7x7 grid.")
        print("For example, if you write '4,6' and hit enter/return,")
        print("you will select line 4, cell 6.")
        print("There are six ships altogether.")
        print()
        print("Three ships are vertically aligned,")
        print("and three are horizontally aligned.")
        print("Happy hunting!")
        user_input = input()
        if (user_input):
            start_screen()

    # If he wants to exit the game:
    elif (user_input == "exit" or user_input == "e"):
        print("Goodbye...")
        time.sleep(1)
        exit()
    else:
        start_screen()

# Starts the game when file runs:
start_screen()