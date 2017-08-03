import API
import datetime

class Pinky:
    refresh_timer = datetime.timedelta(seconds=5)

    def __refresher(self):
        if datetime.datetime.now() - self.last_refresh > self.refresh_timer:
            print('true refresh')
            self.data = self.api.get_game_state()
            self.last_refresh = datetime.datetime.now()
        else:
            print('fake refresh')
        return self.data

    def __init__(self, email, password):
        self.api = API.TaleAPI()
        self.api.login(email, password)
        self.last_refresh = datetime.datetime.now()
        self.data = self.api.get_game_state()

    def health_percentage(self):
        r = self.__refresher()
        hp = r['account']['hero']['base']['health']
        maxhp = r['account']['hero']['base']['max_health']
        return (hp*100)//maxhp

    def energy_levels(self):
        r = self.__refresher()
        current = r['account']['hero']['energy']
        # dict keys: 'bonus', 'max', 'value', 'discount'
        return current

    def action(self):
        '''
        0: idle
        1: quest
        2: travel
        3: NPC combat
        4: dead
        5: town
        6: healing
        7: equipping
        8: trading
        9: wandering around town
        10: praying
        11: reserved
        12: reserved hero interaction
        13: pvp
        14: reserved for tests
        15: petting the companion
        16: new hero
        '''
        r = self.__refresher()
        return r['account']['hero']['action']['type']

    def is_alive(self):
        r = self.__refresher()
        return r['account']['hero']['base']['alive']

    def bag_is_full(self):
        r = self.__refresher()
        return r['account']['hero']['secondary']['max_bag_size'] == r['account']['hero']['secondary']['loot_items_count']

    def intervention(self):
        self.api.use_ability('help')

