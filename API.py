import requests
import taleAPISettings


class TaleAPI:
    def __init__(self, host=taleAPISettings.HOST, app_id=taleAPISettings.CLIENT, apiver=taleAPISettings.APIVER):
        """
        Construct the api object.

        :param host: hostname
        :param app_id: application identifier
        """
        self.session = requests.session()
        self.host = host
        self.client = app_id
        self.apiver = apiver
        self.url = 'http://' + self.host
        self.csrf = None
        self.session.headers.update({'X-CSRFToken': self.csrf})
        self.sessionid = None
        self.general_settings = {'api_version': self.apiver, 'api_client': self.client}
        '''
        Establish connection, set tokens and session'''
        self.get_game_state()

    def __send_request(self, method, path, headers=None, parameters=None, data=None, methodver=None):
        """
        Sends request.

        :param method: 'get', 'post' etc http methods
        :param headers: dict
        :param parameters: dict {'key': 'val', 'key1' : ['val1', 'val2']}
        :return: response
        """
        call = getattr(self.session, method)
        if headers:
            self.session.headers.update(headers)
        pl = self.general_settings.copy()
        pl.update({'csrfmiddlewaretoken': self.csrf})
        if parameters:
            pl.update(parameters)
        if methodver:
            pl.update({'api_version': methodver})
        r = call(self.url+path, data=data, params=pl, cookies={'sessionid': self.sessionid, 'csrftoken': self.csrf})
        '''if r.json()['status'] == 'error':
            return r
        if not self.sessionid:
            self.sessionid = r.cookies['sessionid']
        if not self.csrf:
            self.csrf = r.cookies['csrftoken']
            self.session.headers.update({'X-CSRFToken': self.csrf})'''
        return r

    def _response(self, resp):
        jsn = resp.json()
        #print(jsn['status'] + ' --- ' + 'None' if jsn['status'] != 'error' else jsn['code'])
        if jsn['status'] == 'error' and jsn['code'] != 'common.csrf':
            raise Exception('Server responded with error' +
                            '\ncode: ' + jsn['code'] +
                            '\nmessage:\n' + jsn['error'] +
                            (('\ndata:\n' + jsn['data']) if 'data' in jsn.keys() else '\nNo data'))
        if 'csrftoken' in resp.cookies:
            self.csrf = resp.cookies['csrftoken']
            self.session.headers.update({'X-CSRFToken': self.csrf})
        if 'sessionid' in resp.cookies:
            self.sessionid = resp.cookies['sessionid']
        #print(jsn)
        return jsn['data'] if 'data' in jsn.keys() else {}

    def login(self, email, password):
        credentials = {'email': email, 'password': password}
        r = self.__send_request('post', '/accounts/auth/api/login', data=credentials)
        return self._response(r)

    def logout(self):
        r = self.__send_request('post', '/accounts/auth/api/logout')
        return self._response(r)

    def get_game_state(self):
        r = self.__send_request('get', '/game/api/info')
        return self._response(r)

    def use_ability(self, abilityid, building=None, battle=None):
        d = {}
        if building:
            d['building'] = building
        elif battle:
            d['battle'] = battle
        r = self.__send_request('post', '/game/abilities/{}/api/use'.format(abilityid), data=d)
        return self._response(r)

    def quest_choice(self, option_uid):
        r = self.__send_request('post', '/game/quests/api/choose/', parameters={'option_uid': option_uid})
        return self._response(r)


