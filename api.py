from requests import Session
from calendar import monthrange
from datetime import timedelta


def monthdelta(date, delta):
    m, y = (date.month - delta) % 12, date.year + (date.month - delta - 1) // 12
    if not m:
        m = 12
    d = min(date.day, monthrange(y, m)[1])
    return date.replace(day=d, month=m, year=y)


class DataCollection:
    def __init__(self, api_host):
        self.host = api_host
        self.api = Session()
        self.api.hooks = {'response': lambda r, *args, **kwargs: r.raise_for_status()}
        self.headers = {
            'content-type': 'application/json',
            'X-API-VERSION': '2.0',
            'Authorization': ''}

    def auth_by_token(self, new_token_type, new_access_token):
        self.headers['Authorization'] = '%s %s' % (new_token_type, new_access_token)

    def auth_by_username(self, username, password):
        self.get_token(username, password)

    def get_token(self, username, password):
        url = self.host + '/idsrv/connect/token'
        payload = 'grant_type=password&scope=openid+profile+email+roles+viewer_api+' \
                  'core_logic_facade&response_type=id_token+token&username=%s&' \
                  'password=%s' % (username, password)
        cur_headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'authorization': 'Basic cm8uY2xpZW50OmFtV25Cc3B9dipvfTYkSQ==',
            'X-API-VERSION': '2.0'
        }
        req = self.api.request('POST', url, data=payload, headers=cur_headers)
        token_type = req.json()['token_type']
        access_token = req.json()['access_token']
        self.headers['Authorization'] = '{} {}'.format(token_type, access_token)
        return access_token

    def get_dimension_attributes(self, dim_id, filters=None):
        if filters is not None:
            filters = filters()
        url = self.host + '/datacollection/api/dimensions/%s/attributes' % dim_id
        help(self.api.request)
        req = self.api.request('GET', url, headers=self.headers, json=filters)
        req.raise_for_status()
        return req.json()

    def get_dimension_elements(self, dim_id, filters=None):
        if filters is not None:
            filters = filters()
        url = self.host + '/datacollection/api/dimensions/%s/elements' % dim_id
        req = self.api.request('GET', url, headers=self.headers, json=filters)
        req.raise_for_status()
        return req.json()

    def put_dimension_elements(self, dim_id, data=None, filters=None):
        if data is None:
            data = {}
        if filters is not None:
            filters = filters()
        req_data = {'filter': filters, 'fields': data}
        url = self.host + '/datacollection/api/dimensions/%s/elements' % dim_id
        req = self.api.request('PUT', url, headers=self.headers, json=req_data)
        req.raise_for_status()
        return req.json()

    def post_dimension_elements(self, dim_id, data=None):
        if data is None:
            data = {}
        url = self.host + '/datacollection/api/dimensions/%s/elements' % dim_id
        req = self.api.request('POST', url, headers=self.headers, json=data)
        req.raise_for_status()
        return req.json()

    def delete_dimension_elements(self, dim_id, filters=None):
        if filters is not None:
            filters = filters()
        url = self.host + '/datacollection/api/dimensions/%s/elements' % dim_id
        req = self.api.request('DELETE', url, headers=self.headers, json=filters)
        req.raise_for_status()
        return req.json()

    def post_dimension_elements_search(self, dim_id, filters=None):
        if filters is not None:
            filters = filters()
        url = self.host + '/datacollection/api/dimensions/%s/elements/search' % dim_id
        req = self.api.request('POST', url, headers=self.headers, json=filters)
        req.raise_for_status()
        return req.json()

    def get_dimension_folders(self, dim_id):
        url = self.host + '/datacollection/api/dimensions/%s/folders' % dim_id
        req = self.api.request('GET', url, headers=self.headers)
        req.raise_for_status()
        return req.json()

    def get_dimension_folder_children(self, dim_id, folder_id):
        url = self.host + '/datacollection/api/dimensions/%s/folders/%s/children' % (dim_id,
                                                                                     folder_id)
        req = self.api.request('GET', url, headers=self.headers)
        req.raise_for_status()
        return req.json()

    def get_dimension_level_folders(self, dim_id, level_id):
        url = self.host + '/datacollection/api/dimensions/%s/levels/%s/folders' % (dim_id,
                                                                                   level_id)
        req = self.api.request('GET', url, headers=self.headers)
        req.raise_for_status()
        return req.json()

    def get_dimension_levels(self, dim_id):
        url = self.host + '/datacollection/api/dimensions/%s/levels' % dim_id
        req = self.api.request('GET', url, headers=self.headers)
        req.raise_for_status()
        return req.json()

    def get_dimensions(self):
        url = self.host + '/datacollection/api/dimensions'
        req = self.api.request('GET', url, headers=self.headers)
        req.raise_for_status()
        return req.json()

    def get_measuregroup_elements(self, measure_id, filters=None):
        if filters is not None:
            filters = filters()
        url = self.host + '/datacollection/api/measuregroups/%s/elements' % measure_id
        req = self.api.request('GET', url, headers=self.headers, json=filters)
        req.raise_for_status()
        return req.json()

    def post_measuregroup_elements(self, measure_id, data=None):
        if data is None:
            data = {}
        url = self.host + '/datacollection/api/measuregroups/%s/elements' % measure_id
        req = self.api.request('POST', url, headers=self.headers, json=data)
        req.raise_for_status()
        return req.json()

    def delete_measuregroup_elements(self, measure_id, filters=None):
        if filters is not None:
            filters = filters()
        url = self.host + '/datacollection/api/measuregroups/%s/elements' % measure_id
        req = self.api.request('DELETE', url, headers=self.headers, json=filters)
        req.raise_for_status()
        return req.json()

    def get_measuregroup(self, measure_id):
        url = self.host + '/datacollection/api/measuregroups/%s' % measure_id
        req = self.api.request('GET', url, headers=self.headers)
        req.raise_for_status()
        return req.json()

    def get_measuregroups(self):
        url = self.host + '/datacollection/api/measuregroups'
        req = self.api.request('GET', url, headers=self.headers)
        req.raise_for_status()
        return req.json()

# SPECIAL FUNCTIONS (NO API)

    def transfer_data(self, group_id, cur_date, dim, granularity='month',
                      from_data=None, to_data=None):

        if (from_data is None or to_data is None) and from_data is not to_data:
            raise AttributeError('Необходимо задать агрументы from_data и to_data '
                                 'вместе или оба аргумента не задавать')

        if granularity == 'day':
            past_date = cur_date - timedelta(days=1)
        elif granularity == 'week':
            past_date = cur_date - timedelta(days=7)
        elif granularity in ['month', 'quarter', 'half year', 'year']:
            months = {'month': 1, 'quarter': 3, 'half year': 6, 'year': 12}[granularity]
            past_date = monthdelta(cur_date, months)
        else:
            raise AttributeError('Аргумент granularity указан неверно, примеры данных: '
                                 'day, week, month, quarter, half year, year')

        past_date = past_date.strftime('%Y-%m-%d')
        cur_date = cur_date.strftime('%Y-%m-%d')

        past_filter = [{'value': past_date,
                        'type': 'calendar',
                        'condition': 'equals'}]
        cur_filter = [{'value': cur_date,
                       'type': 'calendar',
                       'condition': 'equals'}]

        template = self.get_measuregroup(group_id)
        dim_exist = False
        for i in template['dimensions'] + [template['measure']]:
            if i['id'] == dim:
                dim_exist = True

        if not dim_exist:
            raise AttributeError('Проверьте данные аргумента dim (ID группы показателей), '
                                 'они не найдёны в указанном описании текущего периода')

        if type(from_data) == str or type(to_data) == str:
            for i in self.post_dimension_elements_search(dim)['elements']:
                if type(from_data) == str:
                    if i['name'].lower() == from_data.lower():
                        from_data = i['id']
                if type(to_data) == str:
                    if i['name'].lower() == to_data.lower():
                        to_data = i['id']

        if type(from_data) == str or type(to_data) == str:
            raise AttributeError('Проверьте данные аргументов from_data и to_data, '
                                 'они не найдены в указанном описании текущего периода')

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

        past_data = self.get_measuregroup_elements(group_id, {'operation': 'and',
                                                              'filters': past_filter})
        self.delete_measuregroup_elements(group_id, {'operation': 'and',
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
                    dimen.append({'Id': i['dimensionId'],
                                  'ElementId': to_data})
                else:
                    dimen.append({'Id': i['dimensionId'],
                                  'ElementId': i['elementId']})

            if elem['measureElements']:
                if elem['measureElements'][0]['measureId'] == dim:
                    measure = {'Id': past_data['measureGroup']['measure']['id'],
                               'ElementId': to_data}
                else:
                    measure = {'Id': past_data['measureGroup']['measure']['id'],
                               'ElementId': elem['measureElements'][0]['elementId']}
            else:
                measure = None

            self.post_measuregroup_elements(group_id, data=[
                {'Value': elem['value'],
                 'Measure': measure,
                 'Dimensions': dimen,
                 'Calendars': [{'Id': past_data['measureGroup']['calendar']['id'],
                                'Name': past_data['measureGroup']['calendar']['name'],
                                'Date': cur_date}]}])

    def get_measures_from_folder(self, dim, *folders):
        name_folders = list(folders)
        dimensions = self.get_dimensions()['dimensions']
        dims_list = list(filter(lambda x: x['id'] == dim or x['name'] == dim, dimensions))
        if dims_list:
            dim_id = dims_list[-1]['id']
        else:
            raise AttributeError('ТАМ ТАКОГО ДИМА')
            # Заполнить

        def subfolder(folder):
            for e in range(len(name_folders)):
                if name_folders[e] == folder['id']:
                    name_folders[e] = folder['name']

            children = self.get_dimension_folder_children(dim_id, folder['id'])['folders']
            if children:
                temp_dict = {}
                for f in children:
                    temp_dict.update(subfolder(f))
                return {folder['name']: temp_dict}
            else:
                return {folder['name']: []}

        levels, result = self.get_dimension_levels(dim_id)['levels'], {}
        level_folders = self.get_dimension_level_folders(dim_id, levels[0]['id'])['folders']
        for i in level_folders:
            result.update(subfolder(i))

        elements = self.get_dimension_elements(dim_id)['elements']
        for elem in elements:
            data = {'id': elem['id'], 'name': elem['name']}
            if elem['path']:
                temp = result.get(elem['path'][0]['folderName'])
                for fld in elem['path'][1:]:
                    temp = temp.get(fld['folderName'])
                if type(temp) is list:
                    temp.append(data)
                else:
                    temp['OTHERS'] = temp.get('OTHERS', [])
                    temp['OTHERS'].append(data)
            else:
                result['OTHERS'] = result.get('OTHERS', [])
                result['OTHERS'].append(data)
        if name_folders:
            temp = result.get(name_folders[0])
            if temp is None:
                raise AttributeError('В указанном измерении не найдена папка ' + name_folders[0])
            for fld in name_folders[1:]:
                if type(temp) is list:
                    raise AttributeError('В указанном измерении не найдена папка ' + fld)
                temp = temp.get(fld)
                if temp is None:
                    raise AttributeError('В указанном измерении не найдена папка ' + fld)
            return temp
        else:
            if not level_folders:
                return result['OTHERS']
            else:
                return result

    def get_measure_data_by_date(self, group_id, cur_date, dim,
                                 granularity='month', from_data=None):
        if from_data is None:
            raise AttributeError("Необходимо задать агрумент from_data")

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
        past_filter = [{'value': past_date,
                        'type': 'calendar',
                        'condition': 'equals'}]
        template = self.get_measuregroup(group_id)
        dim_exist = False
        for i in template['dimensions'] + [template['measure']]:
            if i['id'] == dim:
                dim_exist = True

        if not dim_exist:
            raise AttributeError('Проверьте данные аргумента dim (ID группы показателей), '
                                 'они не найдёны в указанном описании текущего периода')

        if type(from_data) == str:
            for i in self.post_dimension_elements_search(dim)['elements']:
                if type(from_data) == str:
                    if i['name'].lower() == from_data.lower():
                        from_data = i['id']

        if any(map(lambda x: x['id'] == dim, template['dimensions'])):
            if from_data is not None:
                past_filter.append({'value': from_data,
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

        if type(from_data) == str:
            raise AttributeError('Проверьте данные аргумента from_data,'
                                 'он не найден в указанном описании текущего периода')

        past_data = self.get_measuregroup_elements(group_id, {'operation': 'and',
                                                              'filters': past_filter})
        return past_data

    @staticmethod
    def find_attribute_by_unique_name(dimension_element, attribute_unique_name):
        if type(dimension_element) is not dict or type(attribute_unique_name) is not str:
            raise AttributeError("Пожалуйста, проверьте корректность введённых вами данных")
        for attribute in dimension_element["attributes"]:
            if attribute["attributeId"] == attribute_unique_name:
                return attribute

    @staticmethod
    def find_dimension_element_by_predicate(dimension_elements, predicate):
        for element in dimension_elements["elements"]:
            if predicate(element):
                return element

    @staticmethod
    def find_dimension_element_by_attribute(dimension_elements, attribute_unique_name,
                                            attribute_value):
        if type(dimension_elements) is not dict or type(attribute_unique_name) is not str: # or type(attribute_value) is not int:
            raise AttributeError("Пожалуйста, проверьте корректность введённых вами данных")
        def predicate(element):
            attribute = DataCollection.find_attribute_by_unique_name(element, attribute_unique_name)
            return all((attribute is not None, attribute["value"] == attribute_value))

        return DataCollection.find_dimension_element_by_predicate(dimension_elements, predicate)

    @staticmethod
    def find_dimension_element_by_name(dimension_elements, element_name):
        if type(dimension_elements) is not dict or type(element_name) is not str:
            raise AttributeError("Пожалуйста, проверьте корректность введённых вами данных")

        def predicate(element):
            return bool(element["name"] == element_name)

        return DataCollection.find_dimension_element_by_predicate(dimension_elements, predicate)

    @staticmethod
    def find_dimension_element_by_id(dimension_elements, element_id):
        if type(dimension_elements) is not dict or type(element_id) is not int:
            raise AttributeError("Пожалуйста, проверьте корректность введённых вами данных")

        def predicate(element):
            return bool(element["id"] == element_id)

        return DataCollection.find_dimension_element_by_predicate(dimension_elements, predicate)

    @staticmethod
    def prepare_dimension_element_to_insert(dimension_element, attribute_map):
        if type(dimension_element) is not dict or type(attribute_map) is not dict:
            raise AttributeError("Пожалуйста, проверьте корректность введённых вами данных")
        for attribute in dimension_element["attributes"]:
            attribute_id = attribute["attributeId"]
            if attribute_id in attribute_map:
                attribute["value"] = attribute_map[attribute_id]
        return dimension_element
