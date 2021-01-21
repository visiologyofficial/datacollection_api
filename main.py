from requests import Session
from json import dumps
from calendar import monthrange
from datetime import timedelta

token_type = ''
access_token = ''
headers = {
    'X-API-VERSION': '2.0',
    'content-type': 'application/json',
    'Authorization': ''
}
api_session = Session()
api_session.hooks = {'response': lambda r, *args, **kwargs: r.raise_for_status()}


class VDataCollection:
    def __init__(self, api_host):
        self.host = api_host

    def auth_by_username(self, username, password):
        """ Auths user by username&password """
        self.get_token(username, password)

    def get_token(self, username, password):
        """
        Returns token by username&password given.
        Sets token_type and access_token attributes.
        Adds Authorization header.
        """
        url = self.host + "/idsrv/connect/token"
        payload = "grant_type=password&scope=openid+profile+email+roles+viewer_api+" \
                  "core_logic_facade&response_type=id_token+token" \
                  "&username={}&password={}".format(username, password)
        cur_headers = {
            'content-type': "application/x-www-form-urlencoded",
            'authorization': "Basic cm8uY2xpZW50OmFtV25Cc3B9dipvfTYkSQ==",
            'X-API-VERSION': '2.0'
        }
        res = api_session.request("POST", url, data=payload, headers=cur_headers)
        token_type_ = res.json()['token_type']
        access_token_ = res.json()['access_token']
        headers['Authorization'] = '{} {}'.format(token_type_, access_token_)
        return access_token

    def auth_by_token(self, new_token_type, new_access_token):
        """ Auths user by token type and token """
        headers['Authorization'] = '{} {}'.format(new_token_type, new_access_token)

    def get_measuregroups(self):
        url = self.host + '/datacollection/api/measuregroups'
        req = api_session.request('GET', url, headers=headers)
        return req.json()

    def get_description_by_uniquename(self, group_id):
        url = self.host + '/datacollection/api/measuregroups/{}'.format(group_id)
        req = api_session.request('GET', url, headers=headers)
        return req.json()

    def change_element_in_measuregroup(self, group_id, data=None):
        if data is None:
            data = []
        url = self.host + '/datacollection/api/measuregroups/{}/elements'.format(group_id)
        api_session.request('PUT', url, headers=headers, data=dumps(data) if data else '')

    def get_measuregroup_by_uniquename(self, group_id, filters=None):
        if filters is None:
            filters = {}
        url = self.host + '/datacollection/api/measuregroups/{}/elements'.format(group_id)
        req = api_session.request('GET', url, headers=headers,
                                  data=dumps(filters) if filters else '')
        return req.json()

    def post_dimension_by_uniquename(self, group_id, filters=None):
        if filters is None:
            filters = {}
        url = self.host + '/datacollection/api/dimensions/{}/elements/search'.format(group_id)
        req = api_session.request('POST', url, headers=headers,
                                  data=dumps(filters) if filters else '')
        return req.json()

    def post_create_elements(self, group_id, data=None):
        if data is None:
            data = []
        url = self.host + '/datacollection/api/measuregroups/{}/elements'.format(group_id)
        api_session.request('POST', url, headers=headers,
                            data=dumps(data) if data else {})

    def delete_measuregroup_by_uniquename(self, group_id, filters=None):
        if filters is None:
            filters = {}
        url = self.host + '/datacollection/api/measuregroups/{}/elements'.format(group_id)
        api_session.request('DELETE', url, headers=headers, data=dumps(filters) if filters else '')

    def transfer_data(self, group_id, cur_date, dim,
                      granularity='month', from_data=None, to_data=None):
        """
        :param group_id: (str) - ID группы показателей
        :param cur_date: (object datetime.date) - Текущая дата
        :param dim: ID измерения показателей
        :param granularity: (str)='month' - гранулярность между текущим и прошлым периодом
            примеры: day, week, month, quarter, half year, year
        :param from_data: (str)=None - показатель прошлого периода
        :param to_data: (str)=None - показатель текущего периода

        :return: (NoneType)
        """

        if (from_data is None or to_data is None) and from_data is not to_data:
            raise AttributeError("Необходимо задать агрументы from_data и to_data"
                                 " вместе или оба аргумента не задавать")

        def monthdelta(date, delta):
            m, y = (date.month - delta) % 12, date.year + (date.month - delta - 1) // 12
            if not m:
                m = 12
            d = min(date.day, monthrange(y, m)[1])
            return date.replace(day=d, month=m, year=y)

        if granularity == 'day':
            past_date = cur_date - timedelta(days=1)
        elif granularity == 'week':
            past_date = cur_date - timedelta(days=7)
        elif granularity in ['month', 'quarter', 'half year', 'year']:
            months = {'month': 1, 'quarter': 3, 'half year': 6, 'year': 12}[granularity]
            past_date = monthdelta(cur_date, months)
        else:
            raise AttributeError("Аргумент granularity указан неверно, примеры данных: "
                                 "'day', 'week', 'month', 'quarter', 'half year', 'year'")

        past_date = past_date.strftime("%Y-%m-%d")
        cur_date = cur_date.strftime("%Y-%m-%d")

        past_filter = [{'value': past_date,
                        'type': 'calendar',
                        'condition': 'equals'}]
        cur_filter = [{'value': cur_date,
                       'type': 'calendar',
                       'condition': 'equals'}]

        template = self.get_description_by_uniquename(group_id)
        dim_exist = False
        for i in template['dimensions'] + [template['measure']]:
            if i['id'] == dim:
                dim_exist = True

        if not dim_exist:
            raise AttributeError('Проверьте данные аргумента dim (ID группы показателей), '
                                 'они не найдёны в указанном описании текущего периода')

        if type(from_data) == str or type(to_data) == str:
            for i in self.post_dimension_by_uniquename(dim)['elements']:
                if type(from_data) == str:
                    if i['name'].lower() == from_data.lower():
                        from_data = i['id']
                if type(to_data) == str:
                    if i['name'].lower() == to_data.lower():
                        to_data = i['id']

        if any(map(lambda x: x['id'] == dim, template['dimensions'])):
            if from_data is not None:
                past_filter.append({'value': from_data,
                                    'type': 'DimensionId',
                                    'name': dim,
                                    'condition': 'equals'})
                cur_filter.append({'value': to_data,
                                   'type': 'DimensionId',
                                   'name': dim,
                                   'condition': 'equals'})
        elif template['measure'] is not None:
            if template['measure']['id'] == dim:
                if from_data is not None:
                    past_filter.append({'value': from_data,
                                        'type': 'MeasureId',
                                        'name': dim,
                                        'condition': 'equals'})
                    cur_filter.append({'value': to_data,
                                       'type': 'MeasureId',
                                       'name': dim,
                                       'condition': 'equals'})

        if type(from_data) == str or type(to_data) == str:
            raise AttributeError('Проверьте данные аргументов from_data и to_data, '
                                 'они не найдены в указанном описании текущего периода')

        past_data = self.get_measuregroup_by_uniquename(group_id, {'operation': 'and',
                                                                   'filters': past_filter})
        self.delete_measuregroup_by_uniquename(group_id, {
                'operation': 'and',
                'filters': cur_filter})

        for elem in past_data['elements']:
            dop_filter = []
            for i in elem['dimensionElements']:
                if i['dimensionId'] != dim:
                    dop_filter.append({'value': i['elementId'],
                                       'type': 'DimensionId',
                                       'name': i['dimensionId'],
                                       'condition': 'equals'})
            for i in elem['measureElements']:
                if i['measureId'] != dim:
                    dop_filter.append({'value': i['elementId'],
                                       'type': 'MeasureId',
                                       'name': i['measureId'],
                                       'condition': 'equals'})

            dimen = []
            for i in elem['dimensionElements']:
                if i['dimensionId'] == dim:
                    dimen.append({'Id': i['dimensionId'], 'ElementId': to_data})
                else:
                    dimen.append({'Id': i['dimensionId'], 'ElementId': i['elementId']})

            if elem['measureElements']:
                if elem['measureElements'][0]['measureId'] == dim:
                    measure = {'Id': past_data['measureGroup']['measure']['id'],
                               'ElementId': to_data}
                else:
                    measure = {'Id': past_data['measureGroup']['measure']['id'],
                               'ElementId': elem['measureElements'][0]['elementId']}
            else:
                measure = None

            self.post_create_elements(group_id, data=[
                {'Value': elem['value'],
                 'Measure': measure,
                 'Dimensions': dimen,
                 'Calendars': [{'Id': past_data['measureGroup']['calendar']['id'],
                                'Name': past_data['measureGroup']['calendar']['name'],
                                'Date': cur_date}]}])
