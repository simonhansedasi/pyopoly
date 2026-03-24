class Property:
    def __init__(self, name, price, rent, color, rent_tiers=None, house_cost=0,
                 is_go=False, is_l_f_l=False, is_luck=False, is_tax=False,
                 is_jail=False, is_ec=False, is_fp=False, is_ww=False,
                 is_gtj=False, is_railroad=False, is_utility=False):
        self.name = name
        self.price = price
        self.rent = rent          # base rent (legacy / tax amount)
        self.rent_tiers = rent_tiers or []  # [0h, 1h, 2h, 3h, 4h, hotel]
        self.house_cost = house_cost
        self.color = color
        self.owner = None
        self.houses = 0           # 0-4 houses; 5 = hotel
        self.is_mortgaged = False
        self.is_go = is_go
        self.is_l_f_l = is_l_f_l
        self.is_luck = is_luck
        self.is_tax = is_tax
        self.is_jail = is_jail
        self.is_ec = is_ec
        self.is_fp = is_fp
        self.is_ww = is_ww
        self.is_gtj = is_gtj
        self.is_railroad = is_railroad
        self.is_utility = is_utility


class Board:
    def __init__(self):
        self.properties = [
            Property('Go',                    None, None,  'white', is_go=True),
            Property('Feta St',                 60,    2,  'brown', rent_tiers=[2,  10,  30,  90, 160, 250], house_cost=50),
            Property('Little Free Library',   None, None,  'white', is_l_f_l=True),
            Property('Tallinn St',              60,    4,  'brown', rent_tiers=[4,  20,  60, 180, 320, 450], house_cost=50),
            Property('Income Tax',            None,  200,  'white', is_tax=True),
            Property('Reading Rainbow',        200,   25,  'white', is_railroad=True),
            Property('Old Racist Ave',         100,    6,  'lblue', rent_tiers=[6,  30,  90, 270, 400, 550], house_cost=50),
            Property('Luck',                  None, None,  'white', is_luck=True),
            Property('Ben & Jerrys Ave',       100,    6,  'lblue', rent_tiers=[6,  30,  90, 270, 400, 550], house_cost=50),
            Property('Fancy White People Ave', 120,    8,  'lblue', rent_tiers=[8,  40, 100, 300, 450, 600], house_cost=50),
            Property('Minimum Security Resort',None, None, 'white', is_jail=True),
            Property('Charlies Pl',            140,   10, 'purple', rent_tiers=[10,  50, 150, 450, 625, 750], house_cost=100),
            Property('Power Grid',             130,   10,  'white', is_ec=True, is_utility=True),
            Property('States Rights Ave',      140,   10, 'purple', rent_tiers=[10,  50, 150, 450, 625, 750], house_cost=100),
            Property('Tobacco Ln',             160,   12, 'purple', rent_tiers=[12,  60, 180, 500, 700, 900], house_cost=100),
            Property('Cheeststeak Railroad',   200,   25,  'white', is_railroad=True),
            Property('Pocahontas Wy',          180,   14, 'orange', rent_tiers=[14,  70, 200, 550, 750, 950], house_cost=100),
            Property('Little Free Library',   None, None,  'white', is_l_f_l=True),
            Property('Nashville Ave',          180,   14, 'orange', rent_tiers=[14,  70, 200, 550, 750, 950], house_cost=100),
            Property('Haarlem',                200,   16, 'orange', rent_tiers=[16,  80, 220, 600, 800,1000], house_cost=100),
            Property('Free Parking',          None, None,  'white', is_fp=True),
            Property('Kentucky Fried Chicken', 220,   18,    'red', rent_tiers=[18,  90, 250, 700, 875,1050], house_cost=150),
            Property('Luck',                  None, None,  'white', is_luck=True),
            Property('Sasparilla Mkt',         220,   18,    'red', rent_tiers=[18,  90, 250, 700, 875,1050], house_cost=150),
            Property('Land O Lincoln',         240,   20,    'red', rent_tiers=[20, 100, 300, 750, 925,1100], house_cost=150),
            Property('Stinky Railroad',        200,   25,  'white', is_railroad=True),
            Property('Atlantic City',          260,   22, 'yellow', rent_tiers=[22, 110, 330, 800, 975,1150], house_cost=150),
            Property('Darth Vader',            260,   22, 'yellow', rent_tiers=[22, 110, 330, 800, 975,1150], house_cost=150),
            Property('Pumphouse',              150,   10,  'white', is_ww=True, is_utility=True),
            Property('Martins Fartens',        280,   24, 'yellow', rent_tiers=[24, 120, 360, 850,1025,1200], house_cost=150),
            Property('SEC Investigation',     None, None,  'white', is_gtj=True),
            Property('Birken-no-socks St',     300,   26,  'green', rent_tiers=[26, 130, 390, 900,1100,1275], house_cost=200),
            Property('Beach Ave',              300,   26,  'green', rent_tiers=[26, 130, 390, 900,1100,1275], house_cost=200),
            Property('Little Free Library',   None, None,  'white', is_l_f_l=True),
            Property('The White House',        320,   28,  'green', rent_tiers=[28, 150, 450,1000,1200,1400], house_cost=200),
            Property('Shawty Railroad',        200,   25,  'white', is_railroad=True),
            Property('Luck',                  None, None,  'white', is_luck=True),
            Property('Queen Anne',             350,   35,  'dblue', rent_tiers=[35, 175, 500,1100,1300,1500], house_cost=200),
            Property('Luxury Tax',            None,   75,  'white', is_tax=True),
            Property('Empire St Bldg',         400,   50,  'dblue', rent_tiers=[50, 200, 600,1400,1700,2000], house_cost=200),
        ]
        self.num_tiles = len(self.properties)

        self.color_groups = {
            c: [p for p in self.properties if p.color == c]
            for c in ('brown', 'lblue', 'purple', 'orange', 'red', 'yellow', 'green', 'dblue')
        }

    def get_tile(self, position):
        return self.properties[position % self.num_tiles]

    def has_monopoly(self, player, color):
        if player is None:
            return False
        group = self.color_groups.get(color, [])
        return bool(group) and all(p.owner == player for p in group)

    def railroads_owned_by(self, player):
        return sum(1 for p in self.properties if p.is_railroad and p.owner == player)

    def utilities_owned_by(self, player):
        return sum(1 for p in self.properties if p.is_utility and p.owner == player)

    def railroad_positions(self):
        return [i for i, p in enumerate(self.properties) if p.is_railroad]
