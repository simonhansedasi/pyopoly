import random
import gamefile as gf

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500
        self.in_jail = False


def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

        
        
# class Property:
#     def __init__(self, name, price, rent, color, is_go=False, is_l_f_l=False, is_luck=False, is_tax=False, is_jail=False, is_ec=False, is_fp=False, is_ww=False, is_gtj=False):
#         self.name = name
#         self.price = price
#         self.rent = rent
#         self.color = color
#         self.owner = None
#         self.is_go = is_go
#         self.is_l_f_l = is_l_f_l
#         self.is_luck = is_luck
#         self.is_tax = is_tax
#         self.is_jail = is_jail
#         self.is_ec = is_ec
#         self.is_fp = is_fp
#         self.is_ww = is_ww
#         self.is_gtj = is_gtj

# class Board:
#     def __init__(self):
#         self.properties = [
#             Property('Go', None, None, 'white', is_go=True),
#             Property('Feta St', 60, 2, 'brown'),
#             Property('Little Free Library', None, None, 'white', is_l_f_l=True),
#             Property('Tallinn St', 60, 4, 'brown'),
#             Property('Income Tax',None, 200, 'white', is_tax=True),
#             Property('Reading Rainbow', 200, 25, 'white'),
#             Property('Old Racist Ave', 100, 6, 'lblue'),
#             Property('Luck', None, None, 'white', is_luck=True),
#             Property('Ben & Jerrys Ave', 100, 6, 'lblue'),
#             Property('Fancy White People Ave', 120, 8, 'lblue'),
#             Property('Minimum Security Resort', None,None, 'white',is_jail=True),
#             Property('Charlies Pl', 140, 10, 'purple'),
#             Property('Power Grid', 130, 10, 'white',is_ec=True),
#             Property('States Rights Ave', 140, 10, 'purple'),
#             Property('Tobacco Ln', 160, 12, 'purple'),
#             Property('Cheeststeak Railroad', 200, 25, 'white'),           
#             Property('Pocahontas Wy', 180, 14, 'orange'),
#             Property('Little Free Library', None, None, 'white', is_l_f_l=True),
#             Property('Nashville Ave', 180, 14, 'orange'),
#             Property('Haarlem', 200, 16, 'orange'),
#             Property('Free Parking', None, None, 'white', is_fp=True),
#             Property('Kentucky Fried Chicken', 220, 18, 'red'),
#             Property('Luck', None, None, 'white', is_luck=True),
#             Property('Sasparilla Mkt', 220, 18, 'red'),
#             Property('Land O Lincoln', 240, 20, 'red'),
#             Property('Stinky Railroad', 200, 25, 'white'),           
#             Property('Atlantic City', 260, 22, 'yellow'),
#             Property('Darth Vader', 260, 22, 'yellow'),
#             Property('Pumphouse', 150, 10, 'white',is_ww=True),
#             Property('Martins Fartens', 280, 24, 'yellow'),
#             Property('SEC Investigation', None, None, 'white',is_gtj=True),
#             Property('Birken-no-socks St', 300, 26, 'green'),
#             Property('Beach Ave', 300, 26, 'green'),
#             Property('Little Free Library', None, None, 'white', is_l_f_l=True),
#             Property('The White House', 320, 28, 'green'),
#             Property('Shawty Railroad', 200, 25, 'white'),           
#             Property('Luck', None, None, 'white', is_luck=True),
#             Property('Queen Anne', 350, 35, 'dblue'),
#             Property('Luxury Tax',None, 75, 'white', is_tax=True),
#             Property('Empire St Bldg', 400, 50, 'dblue'),

#         ]
#         self.num_tiles = len(self.properties)

#     def get_tile(self, position):
#         return self.properties[position % self.num_tiles]

def print_colored(text, color):
    colors = {
        'brown': '\033[0;33m',
        'lblue':  '\033[0;36m',
        'purple': '\033[0;35m',
        'orange': '\033[0;33m',
        'red': '\033[0;31m',
        'yellow': '\033[0;33m',
        'green': '\033[0;32m',
        'dblue': '\033[0;94m',
                
        'white': '\033[0;37m'
    }
    reset = '\033[0m'
    if color in colors:
        return colors[color] + text + reset
    else:
        return text

def main():
    board = gf.Board()
    players = [Player('Player 1'), Player('Player 2')]
    num_players = len(players)
    current_player = 0

    while True:
        print(f'{players[current_player].name}`s turn. Current Money: ${players[current_player].money}')
        # print('properties owned:')
        # for property in board.properties:
        #     if property.owner == players[current_player]:
        #         print(f'{print_colored(property.name,property.color)}')
        
        
        #check if player is in jail
        if players[current_player].in_jail:
            print('You are in jail')
            choice = input('Do you want to pay $50 bail? (y/n):')
            if choice.lower() == 'y':
                players[current_player].money -= 50
                players[current_player].in_jail = False
                print(f'{players[current_player].name} paid bail')
                
                dice1,dice2 = roll_dice()
                total_roll = dice1 + dice2
                players[current_player].position += total_roll

                current_property = board.get_tile(players[current_player].position)
                print(f'Landed on: {print_colored(current_property.name, current_property.color)}')
                
                
            else:
                print('Rolling doubles')
                dice1,dice2 = roll_dice()
                if dice1 == dice2:
                    print('Doubles!')
                    players[current_player].in_jail = False
                    total_roll = dice1 + dice2
                    players[current_player].position += total_roll

                    current_property = board.get_tile(players[current_player].position)
                    print(f'Landed on: {print_colored(current_property.name, current_property.color)}')
        else:
            # Options on turn
            while True:
                print('p: View properties / r: roll dice')
                option = input('Select option:')
                # input('Press Enter to roll the dice...')
                print('')
                if option == 'p':
                    print('properties owned:')
                    for property in board.properties:
                        if property.owner == players[current_player]:
                            print(f'{print_colored(property.name,property.color)}')
                if option == 'r':
                    break
                
                else:
                    print('invalid option')

            # elif option

            dice1, dice2 = roll_dice()
            total_roll = dice1 + dice2
            print(f'Rolled {dice1} and {dice2}, moving {total_roll} spaces.')
            previous_position = players[current_player].position  # Store previous position

            players[current_player].position += total_roll
            current_property = board.get_tile(players[current_player].position)
            print(f'Landed on: {print_colored(current_property.name, current_property.color)}')

        if current_property.is_go or players[current_player].position < previous_position:
            players[current_player].money += 200
            print(f'{players[current_player].name} passed Go and received $200.')
        if current_property.is_l_f_l:
            print(f'{players[current_player].name} drew a Little Free Library card.')
            # Implement Little Free Library logic here
        if current_property.is_luck:
            print(f'{players[current_player].name} drew a Luck card.')
            # Implement luck logic here
        else:
            # Handle actions based on the tile landed on
            if current_property.owner is None and current_property.price is not None:
                # Property is not owned (excluding Go), prompt player to buy
                choice = input('Do you want to buy this property? (y/n): ')
                if choice.lower() == 'y':
                    if players[current_player].money >= current_property.price:
                        players[current_player].money -= current_property.price
                        current_property.owner = players[current_player]
                        print(f'{players[current_player].name} bought {current_property.name}')
                    else:
                        print('Not enough money to buy this property.')
                else:
                    print('Property not bought.')
            elif current_property.owner != players[current_player] and current_property.price is not None:
                # Property is owned, pay rent
                rent = current_property.rent
                players[current_player].money -= rent
                current_property.owner.money += rent
                print(f'You paid ${rent} rent to {current_property.owner.name}')

            elif current_property.owner !=players[current_player] and current_property.price is None:
                if current_property.name == 'Income Tax':
                    players[current_player].money -= 200
                    print(f'{players[current_player].name} paid $200 for income tax')

                elif current_property.name == 'Luxury Tax':
                    players[current_player].money -= 75
                    print(f'{players[current_player].name} paid $75 for income tax')

                elif current_property.name == 'Free Parking':
                    players[current_player].money -= 0
                    print(f'{players[current_player].name} paid $0 for parking')



                elif current_property.name == 'Go To Jail':
                    players[current_player].position = 10
                    print(f'{players[current_player].name} is in jail until doubles are rolled or pay $50')
                    players[current_player].in_jail = True
                pass

        print('')
        # Switch to the next player

        current_player = (current_player + 1) % num_players

if __name__ == '__main__':
    main()
