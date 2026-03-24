import random
import time
import gamefile as gf

# ── ANSI color codes ──────────────────────────────────────────────────────────
C = {
    'brown':  '\033[38;5;130m',
    'lblue':  '\033[0;96m',
    'purple': '\033[0;95m',
    'orange': '\033[38;5;208m',
    'red':    '\033[0;91m',
    'yellow': '\033[0;93m',
    'green':  '\033[0;92m',
    'dblue':  '\033[0;94m',
    'white':  '\033[0;97m',
    'bold':   '\033[1m',
    'dim':    '\033[2m',
    'reset':  '\033[0m',
}

COLOR_NAMES = {
    'brown': 'Brown', 'lblue': 'Lt Blue', 'purple': 'Purple',
    'orange': 'Orange', 'red': 'Red', 'yellow': 'Yellow',
    'green': 'Green', 'dblue': 'Dk Blue',
}

def clr(text, color):
    return C.get(color, '') + str(text) + C['reset']

def bold(text):
    return C['bold'] + str(text) + C['reset']

def dim(text):
    return C['dim'] + str(text) + C['reset']

def sep(char='─', width=62):
    print(dim(char * width))

def header(text, width=62):
    print()
    print(dim('═' * width))
    print(bold(f'  {text}'))
    print(dim('═' * width))


# ── Card decks ────────────────────────────────────────────────────────────────

LUCK_CARDS = [
    {'text': 'Bank error in your favor. Collect $200.',              'action': 'collect',        'amount': 200},
    {'text': 'Advance to Go. Collect $200.',                         'action': 'advance_go'},
    {'text': "You've won a beauty contest. Collect $10.",            'action': 'collect',        'amount': 10},
    {'text': "Doctor's fee. Pay $50.",                               'action': 'pay',            'amount': 50},
    {'text': 'Street repairs: $25/house, $100/hotel.',               'action': 'repairs',        'house': 25, 'hotel': 100},
    {'text': 'Speeding fine. Pay $15.',                              'action': 'pay',            'amount': 15},
    {'text': 'Stock rally! Collect $100.',                           'action': 'collect',        'amount': 100},
    {'text': 'Go to Jail. Do not pass Go.',                          'action': 'go_to_jail'},
    {'text': 'Get Out of Jail Free.',                                'action': 'jail_free'},
    {'text': 'Pay hospital fees of $100.',                           'action': 'pay',            'amount': 100},
    {"text": "It's your birthday! Collect $10 from every player.",   'action': 'birthday',       'amount': 10},
    {'text': 'Advance to nearest railroad.',                         'action': 'nearest_railroad'},
]

LFL_CARDS = [
    {'text': 'Community fund: Collect $100.',                        'action': 'collect',        'amount': 100},
    {'text': 'Advance to Go. Collect $200.',                         'action': 'advance_go'},
    {'text': 'Income tax refund. Collect $20.',                      'action': 'collect',        'amount': 20},
    {'text': 'Life insurance matures. Collect $100.',                'action': 'collect',        'amount': 100},
    {'text': 'Pay school fees of $150.',                             'action': 'pay',            'amount': 150},
    {'text': 'Hospital fees. Pay $50.',                              'action': 'pay',            'amount': 50},
    {'text': 'You inherit $100.',                                    'action': 'collect',        'amount': 100},
    {'text': 'Stock sale nets $50.',                                 'action': 'collect',        'amount': 50},
    {'text': 'Go to Jail. Do not pass Go.',                          'action': 'go_to_jail'},
    {'text': 'Get Out of Jail Free.',                                'action': 'jail_free'},
    {'text': 'Second prize in beauty contest. Collect $10.',         'action': 'collect',        'amount': 10},
    {'text': 'Grand Opera Night: Collect $50 from every player.',    'action': 'collect_from_all','amount': 50},
]


class CardDeck:
    def __init__(self, cards):
        self.cards = cards[:]
        random.shuffle(self.cards)
        self.idx = 0

    def draw(self):
        card = self.cards[self.idx % len(self.cards)]
        self.idx += 1
        return card


# ── Player ────────────────────────────────────────────────────────────────────

class Player:
    def __init__(self, name, is_cpu=False):
        self.name = name
        self.is_cpu = is_cpu
        self.position = 0
        self.money = 1500
        self.in_jail = False
        self.jail_turns = 0
        self.jail_free_cards = 0
        self.doubles_count = 0
        self.bankrupt = False

    def __repr__(self):
        return self.name


# ── Display ───────────────────────────────────────────────────────────────────

def prop_str(prop, with_houses=True):
    """Colored property name with optional house/hotel marker."""
    s = clr(prop.name, prop.color)
    if with_houses and prop.houses:
        if prop.houses == 5:
            s += clr(' [HTL]', 'green')
        else:
            s += clr(f' [{"♦"*prop.houses}]', 'yellow')
    if prop.is_mortgaged:
        s += dim(' [MORT]')
    return s


def show_player_status(player, board):
    header(f'{player.name}  —  Cash: ${player.money}')
    tile = board.get_tile(player.position)
    loc = clr('JAIL', 'red') if player.in_jail else clr(tile.name, tile.color)
    print(f'  Location : {loc}  (pos {player.position})')
    if player.jail_free_cards:
        print(f'  GOOJF cards: {player.jail_free_cards}')

    owned = [p for p in board.properties if p.owner == player]
    if not owned:
        print('  No properties owned.')
    else:
        print(f'  Properties ({len(owned)}):')
        for p in owned:
            houses_str = ''
            if p.houses == 5:
                houses_str = clr('  [HOTEL]', 'green')
            elif p.houses:
                houses_str = clr(f'  [{"♦"*p.houses}]', 'yellow')
            mort_str = dim('  [MORTGAGED]') if p.is_mortgaged else ''
            print(f'    {clr(p.name, p.color)}{houses_str}{mort_str}')

    nw = net_worth(player, board)
    print(f'  Net worth: ~${nw}')


def show_board(board):
    header('BOARD OWNERSHIP')
    buyable = ['brown', 'lblue', 'purple', 'orange', 'red', 'yellow', 'green', 'dblue']
    for color in buyable:
        label = COLOR_NAMES[color]
        group = board.color_groups[color]
        line = clr(f'  {label:<8}', color)
        for p in group:
            owner = f'({p.owner.name})' if p.owner else '(bank)'
            houses_str = ''
            if p.houses == 5:
                houses_str = clr('[H]', 'green')
            elif p.houses:
                houses_str = clr('♦' * p.houses, 'yellow')
            mort_str = dim('[M]') if p.is_mortgaged else ''
            line += f'  {clr(p.name, color)}{houses_str}{mort_str} {dim(owner)}'
        print(line)
    print()
    rr = [p for p in board.properties if p.is_railroad]
    print('  ' + clr('Railroads:', 'white') + '  ' + '  '.join(
        f'{p.name} {dim("("+p.owner.name+")") if p.owner else dim("(bank)")}' for p in rr))
    ut = [p for p in board.properties if p.is_utility]
    print('  ' + clr('Utilities:', 'white') + '  ' + '  '.join(
        f'{p.name} {dim("("+p.owner.name+")") if p.owner else dim("(bank)")}' for p in ut))


def show_all_players(players, board):
    header('ALL PLAYERS')
    for p in players:
        if p.bankrupt:
            print(f'  {bold(p.name)}: ' + clr('BANKRUPT', 'red'))
            continue
        tile = board.get_tile(p.position)
        jail_str = clr(' [JAIL]', 'red') if p.in_jail else ''
        props = sum(1 for prop in board.properties if prop.owner == p)
        print(f'  {bold(p.name)}: ${p.money:<6}  pos={p.position:<3} {clr(tile.name, tile.color)}{jail_str}  props={props}')


# ── Core mechanics ────────────────────────────────────────────────────────────

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)


def net_worth(player, board):
    owned = [p for p in board.properties if p.owner == player and p.price]
    return player.money + sum(
        (p.price // 2 if p.is_mortgaged else p.price) + p.houses * p.house_cost
        for p in owned
    )


def calc_rent(prop, board, dice_total):
    if prop.is_mortgaged:
        return 0
    if prop.is_railroad:
        n = board.railroads_owned_by(prop.owner)
        return 25 * (2 ** (n - 1))
    if prop.is_utility:
        n = board.utilities_owned_by(prop.owner)
        mult = 10 if n == 2 else 4
        return mult * dice_total
    if prop.rent_tiers:
        rent = prop.rent_tiers[prop.houses]
        if prop.houses == 0 and board.has_monopoly(prop.owner, prop.color):
            rent *= 2
        return rent
    return prop.rent or 0


def send_to_jail(player):
    player.in_jail = True
    player.jail_turns = 0
    player.doubles_count = 0
    player.position = 10
    print(f'  {bold(player.name)} is sent to Minimum Security Resort!')


def can_build(prop, player, board):
    if prop.owner != player or not prop.rent_tiers or prop.is_mortgaged or prop.houses >= 5:
        return False
    if not board.has_monopoly(player, prop.color):
        return False
    group = board.color_groups[prop.color]
    return prop.houses <= min(p.houses for p in group)


def can_sell_house(prop, player, board):
    if prop.owner != player or prop.houses == 0:
        return False
    group = board.color_groups.get(prop.color, [])
    if not group:
        return True
    return prop.houses >= max(p.houses for p in group)


# ── Bankruptcy & mortgaging ───────────────────────────────────────────────────

def raise_funds_cpu(player, need, board):
    """CPU mortgages cheapest un-mortgaged properties to cover `need`."""
    candidates = sorted(
        [p for p in board.properties if p.owner == player and not p.is_mortgaged and p.houses == 0 and p.price],
        key=lambda p: p.price
    )
    for p in candidates:
        if player.money >= need:
            break
        p.is_mortgaged = True
        player.money += p.price // 2
        print(f'  {player.name} mortgages {clr(p.name, p.color)} for ${p.price // 2}.')


def raise_funds_human(player, need, board):
    """Human can sell houses then mortgage properties to cover `need`."""
    print(f'\n  {clr("SHORT ON CASH!", "red")} Need ${need}, have ${player.money}.')

    # Sell houses first
    while True:
        with_houses = [p for p in board.properties if p.owner == player and p.houses > 0]
        if not with_houses:
            break
        print('\n  Sell houses to raise cash? (or press Enter to skip)')
        for i, p in enumerate(with_houses):
            label = 'hotel' if p.houses == 5 else f'{p.houses} house(s)'
            print(f'    {i+1}. {clr(p.name, p.color)} ({label}) → sell 1 for ${p.house_cost // 2}')
        print('    0. Stop selling')
        ch = input('  > ').strip()
        if ch == '0' or ch == '':
            break
        try:
            idx = int(ch) - 1
            if 0 <= idx < len(with_houses):
                p = with_houses[idx]
                p.houses -= 1
                player.money += p.house_cost // 2
                print(f'  Sold. ${player.money} cash now.')
                if player.money >= need:
                    return
        except ValueError:
            pass

    # Mortgage properties
    while player.money < need:
        candidates = [p for p in board.properties if p.owner == player and not p.is_mortgaged and p.price]
        if not candidates:
            break
        print('\n  Mortgage a property?')
        for i, p in enumerate(candidates):
            print(f'    {i+1}. {clr(p.name, p.color)} → ${p.price // 2}')
        print('    0. Give up (declare bankruptcy)')
        ch = input('  > ').strip()
        if ch == '0' or ch == '':
            break
        try:
            idx = int(ch) - 1
            if 0 <= idx < len(candidates):
                p = candidates[idx]
                p.is_mortgaged = True
                player.money += p.price // 2
                print(f'  Mortgaged {clr(p.name, p.color)} for ${p.price // 2}. Cash: ${player.money}')
        except ValueError:
            pass


def handle_debt(player, amount, creditor, board, players):
    """
    Make player pay `amount` to `creditor` (None = bank).
    Returns True if player went bankrupt.
    """
    if player.money >= amount:
        player.money -= amount
        if creditor:
            creditor.money += amount
        return False

    # Try to raise funds
    if player.is_cpu:
        raise_funds_cpu(player, amount, board)
    else:
        raise_funds_human(player, amount, board)

    if player.money >= amount:
        player.money -= amount
        if creditor:
            creditor.money += amount
        return False

    # Truly bankrupt
    print(f'\n  {bold(player.name + " is BANKRUPT!")}')
    player.bankrupt = True
    owned = [p for p in board.properties if p.owner == player]
    for p in owned:
        p.owner = creditor
        p.is_mortgaged = False
        p.houses = 0
        if creditor:
            print(f'  {clr(p.name, p.color)} → {creditor.name}')
        else:
            print(f'  {clr(p.name, p.color)} returned to bank.')
    if creditor:
        creditor.money += player.money
    player.money = 0
    return True


# ── Card application ──────────────────────────────────────────────────────────

def apply_card(card, player, players, board, luck_deck, lfl_deck):
    print(f'\n  {clr("CARD:", "yellow")} "{card["text"]}"')
    action = card['action']

    if action == 'collect':
        player.money += card['amount']
        print(f'  {player.name} collects ${card["amount"]}.')

    elif action == 'pay':
        handle_debt(player, card['amount'], None, board, players)

    elif action == 'advance_go':
        player.position = 0
        player.money += 200
        print(f'  {player.name} advances to Go and collects $200.')

    elif action == 'go_to_jail':
        send_to_jail(player)

    elif action == 'jail_free':
        player.jail_free_cards += 1
        print(f'  {player.name} receives a Get Out of Jail Free card!')

    elif action == 'repairs':
        owned = [p for p in board.properties if p.owner == player]
        total = sum(
            card['hotel'] if p.houses == 5 else p.houses * card['house']
            for p in owned
        )
        if total:
            handle_debt(player, total, None, board, players)
            print(f'  {player.name} pays ${total} in repairs.')
        else:
            print('  No buildings to repair.')

    elif action == 'birthday':
        amt = card['amount']
        for other in players:
            if other != player and not other.bankrupt:
                pay = min(amt, other.money)
                other.money -= pay
                player.money += pay
        print(f'  {player.name} collects ${amt} from each player.')

    elif action == 'collect_from_all':
        amt = card['amount']
        for other in players:
            if other != player and not other.bankrupt:
                pay = min(amt, other.money)
                other.money -= pay
                player.money += pay
        print(f'  {player.name} collects ${amt} from each player.')

    elif action == 'nearest_railroad':
        rr_positions = board.railroad_positions()
        pos = player.position
        nxt = next((r for r in sorted(rr_positions) if r > pos), rr_positions[0])
        if nxt <= pos:  # wrapped
            player.money += 200
            print(f'  {player.name} passes Go! +$200')
        player.position = nxt
        rr = board.get_tile(player.position)
        print(f'  {player.name} advances to {clr(rr.name, rr.color)}.')
        handle_landing(player, rr, players, board, luck_deck, lfl_deck, 0)


# ── Landing logic ─────────────────────────────────────────────────────────────

def handle_landing(player, prop, players, board, luck_deck, lfl_deck, dice_total):
    if prop.is_go:
        pass  # $200 already awarded in movement

    elif prop.is_jail:
        print('  Just visiting Minimum Security Resort.')

    elif prop.is_gtj:
        send_to_jail(player)
        return

    elif prop.is_fp:
        print('  Free Parking. Relax.')

    elif prop.is_tax:
        amt = prop.rent
        print(f'  {player.name} owes ${amt} in tax.')
        handle_debt(player, amt, None, board, players)

    elif prop.is_luck:
        print(f'  {player.name} draws a {clr("Luck", "yellow")} card!')
        apply_card(luck_deck.draw(), player, players, board, luck_deck, lfl_deck)

    elif prop.is_l_f_l:
        print(f'  {player.name} draws a {clr("Little Free Library", "lblue")} card!')
        apply_card(lfl_deck.draw(), player, players, board, luck_deck, lfl_deck)

    elif prop.price is not None:
        if prop.owner is None:
            _handle_unowned(player, prop, players, board, luck_deck, lfl_deck)
        elif prop.owner != player:
            rent = calc_rent(prop, board, dice_total)
            if rent > 0:
                owner_str = clr(prop.owner.name, 'yellow')
                print(f'  {player.name} owes ${rent} rent to {owner_str} for {prop_str(prop, False)}.')
                if not handle_debt(player, rent, prop.owner, board, players):
                    print(f'  Rent of ${rent} paid.')
        else:
            print(f'  You own {prop_str(prop)}.')


def _handle_unowned(player, prop, players, board, luck_deck, lfl_deck):
    if player.is_cpu:
        if player.money - prop.price >= 150:
            player.money -= prop.price
            prop.owner = player
            print(f'  {player.name} buys {clr(prop.name, prop.color)} for ${prop.price}.')
        else:
            print(f'  {player.name} passes on {clr(prop.name, prop.color)}.')
            _auction(prop, players, board)
    else:
        print(f'\n  {prop_str(prop)} is for sale!  Price: ${prop.price}')
        if prop.rent_tiers:
            tiers = prop.rent_tiers
            print(f'  Rents → 0h:${tiers[0]}  1h:${tiers[1]}  2h:${tiers[2]}  '
                  f'3h:${tiers[3]}  4h:${tiers[4]}  hotel:${tiers[5]}')
        elif prop.is_railroad:
            print('  Railroad rents → 1 owned:$25  2:$50  3:$100  4:$200')
        elif prop.is_utility:
            print('  Utility rents → 1 owned: 4×dice  2 owned: 10×dice')
        print(f'  Your cash: ${player.money}')
        ch = input('  Buy? (y/n): ').strip().lower()
        if ch == 'y' and player.money >= prop.price:
            player.money -= prop.price
            prop.owner = player
            print(f'  You bought {clr(prop.name, prop.color)}!')
        elif ch == 'y':
            print('  Not enough cash!')
            _auction(prop, players, board)
        else:
            _auction(prop, players, board)


def _auction(prop, players, board):
    print(f'\n  {clr("AUCTION:", "yellow")} {clr(prop.name, prop.color)} (list ${prop.price})')
    bids = {}
    for p in players:
        if p.bankrupt:
            continue
        if p.is_cpu:
            max_bid = int(prop.price * 0.85)
            if p.money > max_bid + 100:
                bid = random.randint(prop.price // 2, max_bid)
                bids[p] = bid
                print(f'  {p.name} bids ${bid}.')
    human = next((p for p in players if not p.is_cpu and not p.bankrupt), None)
    if human:
        print(f'  Your cash: ${human.money}')
        try:
            bid = int(input('  Your bid (0 = pass): $').strip())
            if 0 < bid <= human.money:
                bids[human] = bid
        except ValueError:
            pass
    if not bids:
        print('  No bids. Property stays with bank.')
        return
    winner = max(bids, key=bids.get)
    winning_bid = bids[winner]
    winner.money -= winning_bid
    prop.owner = winner
    print(f'  {bold(winner.name)} wins the auction for ${winning_bid}!')


# ── Building ──────────────────────────────────────────────────────────────────

def cpu_build(player, board):
    built = True
    while built:
        built = False
        buildable = [
            p for p in board.properties
            if can_build(p, player, board) and player.money >= p.house_cost + 200
        ]
        if buildable:
            p = min(buildable, key=lambda x: x.houses)
            p.houses += 1
            player.money -= p.house_cost
            label = 'hotel' if p.houses == 5 else f'{p.houses} house(s)'
            print(f'  {player.name} builds a {label} on {clr(p.name, p.color)}.')
            built = True


def human_build(player, board):
    while True:
        buildable = [p for p in board.properties if can_build(p, player, board) and player.money >= p.house_cost]
        if not buildable:
            print('  Nothing to build on right now.')
            return
        header('BUILD')
        print(f'  Cash: ${player.money}')
        for i, p in enumerate(buildable):
            next_label = 'hotel' if p.houses == 4 else f'{p.houses+1} house(s)'
            print(f'  {i+1}. {clr(p.name, p.color)} → {next_label}  cost ${p.house_cost}')
        print('  0. Done')
        ch = input('  > ').strip()
        if ch == '0':
            return
        try:
            idx = int(ch) - 1
            if 0 <= idx < len(buildable):
                p = buildable[idx]
                p.houses += 1
                player.money -= p.house_cost
                label = 'hotel' if p.houses == 5 else f'{p.houses} house(s)'
                print(f'  Built! {clr(p.name, p.color)} now has {label}. Cash: ${player.money}')
        except ValueError:
            pass


def human_sell_houses(player, board):
    while True:
        sellable = [p for p in board.properties if can_sell_house(p, player, board)]
        if not sellable:
            print('  No houses/hotels to sell.')
            return
        header('SELL HOUSES/HOTELS')
        for i, p in enumerate(sellable):
            label = 'hotel' if p.houses == 5 else f'{p.houses} house(s)'
            print(f'  {i+1}. {clr(p.name, p.color)} ({label}) → sell 1 for ${p.house_cost // 2}')
        print('  0. Done')
        ch = input('  > ').strip()
        if ch == '0':
            return
        try:
            idx = int(ch) - 1
            if 0 <= idx < len(sellable):
                p = sellable[idx]
                p.houses -= 1
                player.money += p.house_cost // 2
                label = 'hotel' if p.houses == 5 else f'{p.houses} house(s)' if p.houses else 'no buildings'
                print(f'  Sold. {clr(p.name, p.color)} now has {label}. Cash: ${player.money}')
        except ValueError:
            pass


def human_trade(player, players, board):
    """Let the human propose a trade with another player."""
    others = [p for p in players if p != player and not p.bankrupt]
    if not others:
        print('  No other players to trade with.')
        return

    header('TRADE')
    for i, p in enumerate(others):
        props = [prop for prop in board.properties if prop.owner == p and prop.price]
        print(f'  {i+1}. {bold(p.name)}  Cash: ${p.money}  Properties: {len(props)}')
        for prop in props:
            print(f'       {prop_str(prop)}  (${prop.price})')
    print('  0. Cancel')
    ch = input('  Trade with: ').strip()
    if ch == '0' or ch == '':
        return
    try:
        idx = int(ch) - 1
        if not (0 <= idx < len(others)):
            return
    except ValueError:
        return

    target = others[idx]

    # Only unimproved properties can be traded (standard rules)
    my_props = [p for p in board.properties if p.owner == player and p.price and p.houses == 0]
    their_props = [p for p in board.properties if p.owner == target and p.price and p.houses == 0]

    print(f'\n  Negotiating with {bold(target.name)}')

    offer_props = []
    if my_props:
        print('\n  Your properties to offer (space-separated numbers, or Enter for none):')
        for i, p in enumerate(my_props):
            print(f'    {i+1}. {prop_str(p)}  (${p.price})')
        ch = input('  > ').strip()
        for token in ch.split():
            try:
                i = int(token) - 1
                if 0 <= i < len(my_props) and my_props[i] not in offer_props:
                    offer_props.append(my_props[i])
            except ValueError:
                pass

    offer_cash = 0
    try:
        val = input(f'  Cash you offer (0 = none, you have ${player.money}): $').strip()
        offer_cash = max(0, min(int(val), player.money))
    except ValueError:
        pass

    want_props = []
    if their_props:
        print(f'\n  {target.name}\'s properties you want (space-separated numbers, or Enter for none):')
        for i, p in enumerate(their_props):
            print(f'    {i+1}. {prop_str(p)}  (${p.price})')
        ch = input('  > ').strip()
        for token in ch.split():
            try:
                i = int(token) - 1
                if 0 <= i < len(their_props) and their_props[i] not in want_props:
                    want_props.append(their_props[i])
            except ValueError:
                pass

    want_cash = 0
    try:
        val = input(f'  Cash you want from {target.name} (0 = none): $').strip()
        want_cash = max(0, int(val))
    except ValueError:
        pass

    if not offer_props and offer_cash == 0 and not want_props and want_cash == 0:
        print('  Nothing to trade — cancelled.')
        return

    print(f'\n  {bold("Trade Summary:")}')
    offer_str = (', '.join(clr(p.name, p.color) for p in offer_props) or 'nothing') + (f' + ${offer_cash}' if offer_cash else '')
    want_str  = (', '.join(clr(p.name, p.color) for p in want_props)  or 'nothing') + (f' + ${want_cash}'  if want_cash  else '')
    print(f'  You offer : {offer_str}')
    print(f'  You want  : {want_str}')

    if want_cash > target.money:
        print(f'  {target.name} only has ${target.money} — cannot request ${want_cash}.')
        return

    if target.is_cpu:
        accepted = _cpu_evaluate_trade(target, board, offer_props, offer_cash, want_props, want_cash)
        if accepted:
            print(f'  {bold(target.name)} accepts the trade!')
        else:
            print(f'  {bold(target.name)} declines the trade.')
            return
    else:
        ch = input(f'  {target.name}, accept this trade? (y/n): ').strip().lower()
        if ch != 'y':
            print('  Trade declined.')
            return

    for p in offer_props:
        p.owner = target
    for p in want_props:
        p.owner = player
    player.money -= offer_cash
    target.money += offer_cash
    player.money += want_cash
    target.money -= want_cash
    print(f'  {clr("Trade complete!", "green")}')


def _cpu_evaluate_trade(cpu, board, offer_props, offer_cash, want_props, want_cash):
    """CPU accepts/rejects a trade. offer_* = what human gives; want_* = what human receives (cpu loses)."""
    gain_value = sum(p.price for p in offer_props) + offer_cash
    loss_value = sum(p.price for p in want_props) + want_cash

    # Bonus: does receiving these properties complete a CPU monopoly?
    monopoly_bonus = 0
    for p in offer_props:
        group = board.color_groups.get(p.color, [])
        if group:
            after_count = sum(1 for g in group if g.owner == cpu or g in offer_props)
            if after_count == len(group):
                monopoly_bonus += p.price

    # Penalty: does giving these up break a CPU monopoly?
    monopoly_penalty = 0
    for p in want_props:
        group = board.color_groups.get(p.color, [])
        if group and all(g.owner == cpu for g in group):
            monopoly_penalty += p.price * 2

    net = (gain_value + monopoly_bonus) - (loss_value + monopoly_penalty)
    threshold = max(50, loss_value * 0.1)
    return net >= -threshold


def human_mortgage_menu(player, board):
    while True:
        owned = [p for p in board.properties if p.owner == player and p.price]
        if not owned:
            print('  No properties.')
            return
        header('MORTGAGE / UNMORTGAGE')
        print(f'  Cash: ${player.money}')
        for i, p in enumerate(owned):
            if p.is_mortgaged:
                cost = int(p.price * 0.55)
                print(f'  {i+1}. {dim("[MORT]")} {clr(p.name, p.color)} — unmortgage for ${cost}')
            else:
                val = p.price // 2
                house_warn = '  (sell houses first)' if p.houses else ''
                print(f'  {i+1}. {clr(p.name, p.color)} — mortgage for ${val}{house_warn}')
        print('  0. Back')
        ch = input('  > ').strip()
        if ch == '0':
            return
        try:
            idx = int(ch) - 1
            if 0 <= idx < len(owned):
                p = owned[idx]
                if p.is_mortgaged:
                    cost = int(p.price * 0.55)
                    if player.money >= cost:
                        player.money -= cost
                        p.is_mortgaged = False
                        print(f'  Unmortgaged {clr(p.name, p.color)} for ${cost}.')
                    else:
                        print(f'  Need ${cost} to unmortgage.')
                else:
                    if p.houses:
                        print('  Sell buildings first.')
                    else:
                        player.money += p.price // 2
                        p.is_mortgaged = True
                        print(f'  Mortgaged {clr(p.name, p.color)} for ${p.price // 2}.')
        except ValueError:
            pass


# ── Turn logic ────────────────────────────────────────────────────────────────

def move_player(player, dice_total, board):
    """Move player, award Go $200, return landed property."""
    prev = player.position
    player.position = (prev + dice_total) % 40
    if prev + dice_total >= 40:
        player.money += 200
        print(f'  {player.name} passes Go! +$200  (cash: ${player.money})')
    return board.get_tile(player.position)


def do_roll_and_move(player, players, board, luck_deck, lfl_deck):
    """Roll dice, move, land. Returns (doubles, sent_to_jail)."""
    d1, d2 = roll_dice()
    total = d1 + d2
    doubles = d1 == d2
    print(f'  Rolled: {clr(str(d1), "yellow")} + {clr(str(d2), "yellow")} = {bold(str(total))}'
          + (clr('  DOUBLES!', 'green') if doubles else ''))

    if doubles:
        player.doubles_count += 1
        if player.doubles_count == 3:
            print(f'  Three doubles in a row! {clr("GO TO JAIL", "red")}')
            send_to_jail(player)
            return doubles, True
    else:
        player.doubles_count = 0

    prop = move_player(player, total, board)
    print(f'  Landed on: {prop_str(prop)}')
    handle_landing(player, prop, players, board, luck_deck, lfl_deck, total)
    return doubles, player.in_jail


def human_jail_turn(player, players, board, luck_deck, lfl_deck):
    player.jail_turns += 1
    print(f'\n  {clr("IN JAIL", "red")} (turn {player.jail_turns}/3)')

    # Use GOOJF card?
    if player.jail_free_cards:
        ch = input('  Use Get Out of Jail Free card? (y/n): ').strip().lower()
        if ch == 'y':
            player.jail_free_cards -= 1
            player.in_jail = False
            player.jail_turns = 0
            print('  Used GOOJF card!')
            do_roll_and_move(player, players, board, luck_deck, lfl_deck)
            return

    if player.jail_turns >= 3:
        print('  3 turns in jail — must pay $50.')
        player.money -= 50
        player.in_jail = False
        player.jail_turns = 0
        do_roll_and_move(player, players, board, luck_deck, lfl_deck)
        return

    print('  Options:  pay — pay $50 bail   roll — try for doubles')
    ch = input('  > ').strip().lower()
    if ch == 'pay':
        if player.money >= 50:
            player.money -= 50
            player.in_jail = False
            player.jail_turns = 0
            print('  Paid $50 bail — free!')
            do_roll_and_move(player, players, board, luck_deck, lfl_deck)
        else:
            print('  Not enough for bail! Rolling...')
            _jail_roll_doubles(player, players, board, luck_deck, lfl_deck)
    else:
        _jail_roll_doubles(player, players, board, luck_deck, lfl_deck)


def cpu_jail_turn(player, players, board, luck_deck, lfl_deck):
    player.jail_turns += 1
    if player.jail_free_cards:
        player.jail_free_cards -= 1
        player.in_jail = False
        player.jail_turns = 0
        print(f'  {player.name} uses GOOJF card.')
    elif player.jail_turns >= 3 or player.money > 350:
        player.money -= 50
        player.in_jail = False
        player.jail_turns = 0
        print(f'  {player.name} pays $50 bail.')
    else:
        _jail_roll_doubles(player, players, board, luck_deck, lfl_deck)
        return
    if not player.in_jail:
        do_roll_and_move(player, players, board, luck_deck, lfl_deck)


def _jail_roll_doubles(player, players, board, luck_deck, lfl_deck):
    d1, d2 = roll_dice()
    total = d1 + d2
    print(f'  Rolling for doubles: {d1} + {d2}')
    if d1 == d2:
        print(f'  {clr("DOUBLES!", "green")} Free!')
        player.in_jail = False
        player.jail_turns = 0
        prop = move_player(player, total, board)
        print(f'  Landed on: {prop_str(prop)}')
        handle_landing(player, prop, players, board, luck_deck, lfl_deck, total)
    else:
        print(f'  No doubles. {player.name} stays in jail.')


def human_turn(player, players, board, luck_deck, lfl_deck):
    header(f'YOUR TURN  —  {player.name}  —  Cash: ${player.money}')
    tile = board.get_tile(player.position)
    print(f'  Location: {clr(tile.name, tile.color)}  (pos {player.position})')

    while True:
        menu = ['r: Roll', 'p: Properties', 'b: Build', 'm: Mortgage',
                's: Sell houses', 't: Trade', 'a: All players', 'B: Board']
        print('\n  ' + dim('|').join(f'  {o}  ' for o in menu))
        ch = input('  > ').strip()
        if ch == 'r':
            break
        elif ch == 'p':
            show_player_status(player, board)
        elif ch == 'b':
            human_build(player, board)
        elif ch == 'm':
            human_mortgage_menu(player, board)
        elif ch == 's':
            human_sell_houses(player, board)
        elif ch == 't':
            human_trade(player, players, board)
        elif ch == 'a':
            show_all_players(players, board)
        elif ch == 'B':
            show_board(board)
        else:
            print('  Invalid option.')

    if player.in_jail:
        human_jail_turn(player, players, board, luck_deck, lfl_deck)
        return

    doubles, jailed = do_roll_and_move(player, players, board, luck_deck, lfl_deck)
    if doubles and not jailed and not player.bankrupt:
        print(f'\n  {clr("Doubles — roll again!", "green")}')
        human_turn(player, players, board, luck_deck, lfl_deck)


def cpu_turn(player, players, board, luck_deck, lfl_deck):
    header(f'{player.name}\'s TURN  (CPU)  —  Cash: ${player.money}')
    time.sleep(0.4)
    cpu_build(player, board)

    if player.in_jail:
        cpu_jail_turn(player, players, board, luck_deck, lfl_deck)
        return

    doubles, jailed = do_roll_and_move(player, players, board, luck_deck, lfl_deck)
    if doubles and not jailed and not player.bankrupt:
        print(f'\n  {player.name} rolls again (doubles).')
        time.sleep(0.3)
        cpu_turn(player, players, board, luck_deck, lfl_deck)


# ── Win condition ─────────────────────────────────────────────────────────────

def active_players(players):
    return [p for p in players if not p.bankrupt]


def check_winner(players):
    alive = active_players(players)
    return alive[0] if len(alive) == 1 else None


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print('\033[2J\033[H', end='')  # clear screen
    print(clr("""
  ██████  ██    ██  ██████  ██████   ██████  ██      ██    ██
  ██   ██  ██  ██  ██    ██ ██   ██ ██    ██ ██       ██  ██
  ██████    ████   ██    ██ ██████  ██    ██ ██        ████
  ██         ██    ██    ██ ██      ██    ██ ██         ██
  ██         ██     ██████  ██       ██████  ███████    ██
    """, 'green'))
    sep()
    print(bold('  A Monopoly-style CLI game  |  1 human vs 3 CPUs'))
    print(dim('  Buy properties · Build houses · Bankrupt your enemies'))
    sep()

    name = input('\n  Enter your name: ').strip() or 'Player'

    board = gf.Board()
    luck_deck = CardDeck(LUCK_CARDS)
    lfl_deck = CardDeck(LFL_CARDS)

    players = [
        Player(name,                  is_cpu=False),
        Player('CPU - Chomper',       is_cpu=True),
        Player('CPU - Banksy',        is_cpu=True),
        Player('CPU - Foreclosure Phil', is_cpu=True),
    ]

    print(f'\n  Players: {", ".join(bold(p.name) for p in players)}')
    print('  Each player starts with $1,500.')
    input('\n  Press Enter to begin...')

    turn = 0
    MAX_TURNS = 1000

    while turn < MAX_TURNS:
        winner = check_winner(players)
        if winner:
            break

        player = players[turn % len(players)]
        if player.bankrupt:
            turn += 1
            continue

        try:
            if player.is_cpu:
                cpu_turn(player, players, board, luck_deck, lfl_deck)
            else:
                human_turn(player, players, board, luck_deck, lfl_deck)
        except KeyboardInterrupt:
            print('\n\n  Game interrupted.')
            break

        winner = check_winner(players)
        if winner:
            break

        if not player.is_cpu and not player.bankrupt:
            print(f'\n  {dim("End of your turn.")}  Cash: ${player.money}')
            input('  Press Enter for next player...')

        turn += 1

    # ── Game over ──────────────────────────────────────────────────────────────
    header('GAME OVER')
    alive = active_players(players)
    if len(alive) == 1:
        w = alive[0]
        print(f'\n  {clr("🏆  " + w.name + " WINS!", "yellow")}  Final cash: ${w.money}')
    else:
        print('\n  Standings by net worth:')
        ranked = sorted(players, key=lambda p: net_worth(p, board), reverse=True)
        for i, p in enumerate(ranked):
            status = clr('BANKRUPT', 'red') if p.bankrupt else f'${net_worth(p, board)}'
            print(f'  {i+1}. {bold(p.name)}: {status}')
    print()


if __name__ == '__main__':
    main()
