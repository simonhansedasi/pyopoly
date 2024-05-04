import random

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500
        self.in_jail = False


def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

        
        
        
class Property:
    def __init__(self, name, price, rent, color, is_go=False, is_community_chest=False, is_chance=False, is_tax=False, is_jail=False, is_ec=False, is_fp=False, is_ww=False, is_gtj=False):
        self.name = name
        self.price = price
        self.rent = rent
        self.color = color
        self.owner = None
        self.is_go = is_go
        self.is_community_chest = is_community_chest
        self.is_chance = is_chance
        self.is_tax = is_tax
        self.is_jail = is_jail
        self.is_ec = is_ec
        self.is_fp = is_fp
        self.is_ww = is_ww
        self.is_gtj = is_gtj

class Board:
    def __init__(self):
        self.properties = [
            Property('Go', None, None, 'white', is_go=True),
            Property('Mediterranean Ave', 60, 2, 'brown'),
            Property('Community Chest', None, None, 'white', is_community_chest=True),
            Property('Baltic Ave', 60, 4, 'brown'),
            Property('Income Tax',None, 200, 'white', is_tax=True),
            Property('Reading Railroad', 200, 25, 'white'),
            Property('Oriental Ave', 100, 6, 'lblue'),
            Property('Chance', None, None, 'white', is_chance=True),
            Property('Vermont Ave', 100, 6, 'lblue'),
            Property('Connecticut Ave', 120, 8, 'lblue'),
            Property('Jail', None,None, 'white',is_jail=True),
            Property('St Charles Pl', 140, 10, 'purple'),
            Property('Electric Company', 130, 10, 'white',is_ec=True),
            Property('States Ave', 140, 10, 'purple'),
            Property('Virginia Ave', 160, 12, 'purple'),
            Property('Pennsylvania Railroad', 200, 25, 'white'),           
            Property('St James Pl', 180, 14, 'orange'),
            Property('Community Chest', None, None, 'white', is_community_chest=True),
            Property('Tennessee Ave', 180, 14, 'orange'),
            Property('New York Ave', 200, 16, 'orange'),
            Property('Free Parking', None, None, 'white', is_fp=True),
            Property('Kentucky Ave', 220, 18, 'red'),
            Property('Chance', None, None, 'white', is_chance=True),
            Property('Indiana Ave', 220, 18, 'red'),
            Property('Illinois Ave', 240, 20, 'red'),
            Property('B & O Railroad', 200, 25, 'white'),           
            Property('Atlantic Ave', 260, 22, 'yellow'),
            Property('Ventnor Ave', 260, 22, 'yellow'),
            Property('Water Works', 150, 10, 'white',is_ww=True),
            Property('Marvin Gardens', 280, 24, 'yellow'),
            Property('Go To Jail', None, None, 'white',is_gtj=True),
            Property('Pacific Ave', 300, 26, 'green'),
            Property('North Carolina Ave', 300, 26, 'green'),
            Property('Community Chest', None, None, 'white', is_community_chest=True),
            Property('Pennsylvania Ave', 320, 28, 'green'),
            Property('Short Line Railroad', 200, 25, 'white'),           
            Property('Chance', None, None, 'white', is_chance=True),
            Property('Park Pl', 350, 35, 'dblue'),
            Property('Luxury Tax',None, 75, 'white', is_tax=True),
            Property('Boardwalk', 400, 50, 'dblue'),

        ]
        self.num_tiles = len(self.properties)

    def get_tile(self, position):
        return self.properties[position % self.num_tiles]

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
    board = Board()
    players = [Player('Player 1'), Player('Player 2')]
    num_players = len(players)
    current_player = 0

    while True:
        print(f'{players[current_player].name}`s turn. Current Money: ${players[current_player].money}')
        print('properties owned:')
        for property in board.properties:
            if property.owner == players[current_player]:
                print(f'{print_colored(property.name,property.color)}')
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
            input('Press Enter to roll the dice...')
            print('')
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
        if current_property.is_community_chest:
            print(f'{players[current_player].name} drew a Community Chest card.')
            # Implement Community Chest logic here
        if current_property.is_chance:
            print(f'{players[current_player].name} drew a Chance card.')
            # Implement Chance logic here
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
