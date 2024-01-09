



# Function to generate a randomized grid
import random
def make_grid():
    grid = [['~' for _ in range(10)] for _ in range(10)]
    ships = [('M', 3), ('B', 2), ('D', 2), ('S', 3), ('P', 2)]

    for ship, length in ships:
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                x = random.randint(1, 9)
                y = random.randint(0, 9 - length)
                if all(grid[x][y+i] == '~ ' for i in range(length)):
                    for i in range(length):
                        grid[x][y+i] = ship
                    if ship == 'D':

                        grid[x-1][y] = ship
                    if ship == 'B':
                        grid[x-1][y+1] = ship
                        grid[x-1][y] = ship
                    if ship == 'M':
                        grid[x-1][y+1] = ship
                        grid[x+1][y+1] = ship
                    break

            else:
                x = random.randint(0, 9 - length)
                y = random.randint(1, 8)
                if all(grid[x+i][y] == '~' for i in range(length)):
                    for i in range(length):
                        grid[x+i][y] = ship
                    if ship == 'D':

                        grid[x][y+1] = ship
                    if ship == 'B':
                        grid[x][y+1] = ship
                        grid[x+1][y+1] = ship
                    if ship == 'M':
                        grid[x+1][y-1] = ship
                        grid[x+1][y+1] = ship
                    break

    return grid


def make_blank_grid():
    grid = [['~' for _ in range(10)] for _ in range(10)]
    # ships = [(' M ', 5), (' B ', 4), (' D ', 3), (' S ', 3), (' P ', 2)]

    return grid


# Function to print the grid
def print_grid(grid):
    print('   0  1  2  3  4  5  6  7  8  9')
    for i, row in enumerate(grid):
        ss = ''
        print(chr(65 + i) + '  ', end='')

        for cell in row:
            ss = ss + cell + '  '
        ss = ss[:-2]
        print(ss)

        # print()

# Function to check if a target is valid


def is_valid_target(target):
    if len(target) != 2 or not target[0].isalpha() or not target[1].isdigit():
        return False
    row = ord(target[0].upper()) - 65
    col = int(target[1])
    return 0 <= row < 10 and 0 <= col < 10

# Function to update the grid after a shot


def update_grid(grid, target):
    row = ord(target[0].upper()) - 65
    col = int(target[1])
    if grid[row][col] != '~':
        letter = grid[row][col]
        grid[row][col] = 'x'
        return letter
    else:
        grid[row][col] = 'o'
        return False


def update_blank_grid_hit(grid, target):
    row = ord(target[0].upper()) - 65
    col = int(target[1])

    grid[row][col] = 'x'
    return True


def update_blank_grid_miss(grid, target):
    row = ord(target[0].upper()) - 65
    col = int(target[1])

    grid[row][col] = 'o'
    return True


def check_boat(letters, ships):
    for ship, length in ships:

        if letters.count(ship[0]) == length:
            return ship
    return False


# Function to calculate the score
def calculate_score(hits, shots):
    if shots == 0:
        return 0
    return (hits / shots)*100

# Function to update the Hall of Fame


def update_hall_of_fame(player, hits, shots):
    with open('battleship_hof.txt', 'a') as file:
        file.write(f'{player},{hits},{shots-hits}\n')

    # Read the current Hall of Fame records
    '''records = []
    with open('battleship_hof.txt', 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            #player, score = line.strip().split(',')
            records.append(f'{player},{hits},{shots-hits}\n')

    # Sort the records by score in descending order
    records.sort(key=lambda x: x[1], reverse=True)

    # Keep only the top ten records
    records = records[:10]

    # Write the updated Hall of Fame records
    with open('battleship_hof.txt', 'w') as file:
        file.write('Player,Score\n')
        for player, score in records:
            file.write(f'{player},{score}\n')'''

# Function to display the Hall of Fame


def display_hall_of_fame():
    print('')
    print('')
    print('~~~~~~~~ Hall of Fame ~~~~~~~~')
    print('Rank : Accuracy :  Player Name')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    with open('battleship_hof.txt', 'r') as file:
        lines = file.readlines()

        sorted_lines = sorted(
            lines[1:], key=lambda x: x.split(',')[2], reverse=False)
        k = 1
        for line in sorted_lines[0:10]:
            s_line = line.rstrip()
            player, hits, misses = s_line.strip().split(',')
            calc_score = (float(float(hits)/(float(misses)+float(hits)))*100)
            print(f'{k:>4}{calc_score:>10.2f}%{player :>15}')
            k += 1

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

# Main game loop


def main():

    print('')
    print('               ~ Welcome to Battleship! ~               ')
    print('')
    print("ChatGPT has gone rogue and commandeered a space strike\nfleet. It's on a mission to take over the world.  We've\nlocated the stolen ships, but we need your superior\nintelligence to help us destroy them before it's too\nlate.")
    while True:

        print('')

        print('Menu:')
        print('  1 : Instructions')
        print('  2 : View Example Map')
        print('  3 : New Game')
        print('  4 : Hall of Fame')
        print('  5 : Quit')
        choice = input('What would you like to do? ')

        if choice == '1':
            print('Instructions:')
            # Display game instructions here

        elif choice == '2':
            print('')
            example_grid = make_grid()
            print_grid(example_grid)
            print()

        elif choice == '3':
            play_game()

            
        elif choice == '4':
            display_hall_of_fame()

        elif choice == '5':
            print('')
            print('Goodbye')
            print('')
            break

        else:
            print('')
            print('Invalid selection.  Please choose a number from the menu.')


def play_game():
        ships_to_check = [('Mothership', 5), ('Battleship', 4),
                            ('Patrol Ship', 2), ('Stealth Ship', 3), ('Destroyer', 3)]
        # print('New Game:')

        grid = make_grid()
        shots = 0
        hits = 0
        blank_grid = make_blank_grid()
        #print_grid(grid)
        print()
        print_grid(blank_grid)
        print()
        letters = []

        while hits < 17:
            #print(hits)
            target = ''
        
            target = input('Where should we target next (q to quit)? ')
            if target == 'q' or target == 'Q':
                return
            if not is_valid_target(target):
                print('Please enter exactly two characters.')
                continue
            shots += 1
            letter = update_grid(grid, target)
            if letter:
                hits += 1
                print()
                print("IT'S A HIT!")
                
                

                letters.append(letter)

                ship_name = check_boat(letters, ships_to_check)
                if ship_name:
                    print(f"The enemy's {ship_name} has been destroyed.")

                    for x in ships_to_check:

                        if ship_name in x:
                            ships_to_check.remove(x)
                # ships_to_check.remove([ship_name,ship_name.length])

                update_blank_grid_hit(blank_grid, target)
                print()
                if hits <17:
                    print_grid(blank_grid)
                    print()
            else:
                print()
                print('miss')
                # print()
                update_blank_grid_miss(blank_grid, target)
                print()
                print_grid(blank_grid)
                print()

        score = calculate_score(hits, shots)
        print("You've destroyed the enemy fleet!")
        print('Humanity has been saved from the threat of AI.')
        print('')
        print('For now ...')
        print('')
        print(
            f"Congratulations, you have achieved a targeting accuracy\nof {score:.2f}% and earned a spot in the Hall of Fame.")
        player = input('Enter your name: ')

        update_hall_of_fame(player, hits, shots)
        display_hall_of_fame()
        return





"""Do not change anything below this line."""
if __name__ == "__main__":
    main()
