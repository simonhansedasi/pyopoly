class Property:
    def __init__(self, name, price, rent, color, is_go=False, is_l_f_l=False, is_luck=False, is_tax=False, is_jail=False, is_ec=False, is_fp=False, is_ww=False, is_gtj=False):
        self.name = name
        self.price = price
        self.rent = rent
        self.color = color
        self.owner = None
        self.is_go = is_go
        self.is_l_f_l = is_l_f_l
        self.is_luck = is_luck
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
            Property('Feta St', 60, 2, 'brown'),
            Property('Little Free Library', None, None, 'white', is_l_f_l=True),
            Property('Tallinn St', 60, 4, 'brown'),
            Property('Income Tax',None, 200, 'white', is_tax=True),
            Property('Reading Rainbow', 200, 25, 'white'),
            Property('Old Racist Ave', 100, 6, 'lblue'),
            Property('Luck', None, None, 'white', is_luck=True),
            Property('Ben & Jerrys Ave', 100, 6, 'lblue'),
            Property('Fancy White People Ave', 120, 8, 'lblue'),
            Property('Minimum Security Resort', None,None, 'white',is_jail=True),
            Property('Charlies Pl', 140, 10, 'purple'),
            Property('Power Grid', 130, 10, 'white',is_ec=True),
            Property('States Rights Ave', 140, 10, 'purple'),
            Property('Tobacco Ln', 160, 12, 'purple'),
            Property('Cheeststeak Railroad', 200, 25, 'white'),           
            Property('Pocahontas Wy', 180, 14, 'orange'),
            Property('Little Free Library', None, None, 'white', is_l_f_l=True),
            Property('Nashville Ave', 180, 14, 'orange'),
            Property('Haarlem', 200, 16, 'orange'),
            Property('Free Parking', None, None, 'white', is_fp=True),
            Property('Kentucky Fried Chicken', 220, 18, 'red'),
            Property('Luck', None, None, 'white', is_luck=True),
            Property('Sasparilla Mkt', 220, 18, 'red'),
            Property('Land O Lincoln', 240, 20, 'red'),
            Property('Stinky Railroad', 200, 25, 'white'),           
            Property('Atlantic City', 260, 22, 'yellow'),
            Property('Darth Vader', 260, 22, 'yellow'),
            Property('Pumphouse', 150, 10, 'white',is_ww=True),
            Property('Martins Fartens', 280, 24, 'yellow'),
            Property('SEC Investigation', None, None, 'white',is_gtj=True),
            Property('Birken-no-socks St', 300, 26, 'green'),
            Property('Beach Ave', 300, 26, 'green'),
            Property('Little Free Library', None, None, 'white', is_l_f_l=True),
            Property('The White House', 320, 28, 'green'),
            Property('Shawty Railroad', 200, 25, 'white'),           
            Property('Luck', None, None, 'white', is_luck=True),
            Property('Queen Anne', 350, 35, 'dblue'),
            Property('Luxury Tax',None, 75, 'white', is_tax=True),
            Property('Empire St Bldg', 400, 50, 'dblue'),

        ]
        self.num_tiles = len(self.properties)

    def get_tile(self, position):
        return self.properties[position % self.num_tiles]
