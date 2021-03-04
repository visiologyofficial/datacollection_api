from requests import Session, exceptions
from calendar import monthrange
from datetime import timedelta
import filters as fl


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
        if type(filters) is fl.ComplexFilter or issubclass(type(filters), fl.SimpleFilter):
            filters = filters()
        elif filters is not None:
            raise AttributeError('Атрибут filters не является экземпляром наследника'
                                 ' класса SimpleFilter или экземпляром класса ComplexFilter')
        url = self.host + '/datacollection/api/dimensions/%s/attributes' % dim_id
        req = self.api.request('GET', url, headers=self.headers, json=filters)
        req.raise_for_status()
        return req.json()

    def get_dimension_elements(self, dim_id, filters=None):
        if type(filters) is fl.ComplexFilter or issubclass(type(filters), fl.SimpleFilter):
            filters = filters()
        elif filters is not None:
            raise AttributeError('Атрибут filters не является экземпляром наследника'
                                 ' класса SimpleFilter или экземпляром класса ComplexFilter')
        # filters = {"operation": "and", "filters": [{"value": "Иванов", "name": "Фамилия",
        #                                             "type": "attribute", "condition": "equals"}]}
        url = self.host + '/datacollection/api/dimensions/%s/elements' % dim_id
        req = self.api.request('GET', url, headers=self.headers, json=filters)
        req.raise_for_status()
        return req.json()

    def put_dimension_elements(self, dim_id, data=None, filters=None):
        if data is None:
            data = {}
        if type(filters) is fl.ComplexFilter or \
                issubclass(type(filters), fl.SimpleFilter):
            filters = filters()
        elif filters is not None:
            raise AttributeError('Атрибут filters не является экземпляром наследника'
                                 ' класса SimpleFilter или экземпляром класса ComplexFilter')
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
        if type(filters) is fl.ComplexFilter or \
                issubclass(type(filters), fl.SimpleFilter):
            filters = filters()
        url = self.host + '/datacollection/api/dimensions/%s/elements' % dim_id
        req = self.api.request('DELETE', url, headers=self.headers, json=filters)
        req.raise_for_status()
        return req.json()

    def post_dimension_elements_search(self, dim_id, filters=None):
        if type(filters) is fl.ComplexFilter or issubclass(type(filters), fl.SimpleFilter):
            filters = filters()
        elif filters is not None:
            raise AttributeError('Атрибут filters не является экземпляром наследника'
                                 ' класса SimpleFilter или экземпляром класса ComplexFilter')
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
        if type(filters) is fl.ComplexFilter or issubclass(type(filters), fl.SimpleFilter):
            filters = filters()
        elif filters is not None:
            raise AttributeError('Атрибут filters не является экземпляром наследника'
                                 ' класса SimpleFilter или экземпляром класса ComplexFilter')
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
        if type(filters) is fl.ComplexFilter or issubclass(type(filters), fl.SimpleFilter):
            filters = filters()
        elif filters is not None:
            raise AttributeError('Атрибут filters не является экземпляром наследника'
                                 ' класса SimpleFilter или экземпляром класса ComplexFilter')
        url = self.host + '/datacollection/api/measuregroups/%s/elements' % measure_id
        req = self.api.request('DELETE', url, headers=self.headers, json=filters)
        req.raise_for_status()
        return req.json()

    def post_measuregroup_elements_search(self, measure_id, filters=None):
        if type(filters) is fl.ComplexFilter or issubclass(type(filters), fl.SimpleFilter):
            filters = filters()
        elif filters is not None:
            raise AttributeError('Атрибут filters не является экземпляром наследника'
                                 ' класса SimpleFilter или экземпляром класса ComplexFilter')
        url = self.host + '/datacollection/api/measuregroups/%s/elements/search' % measure_id
        req = self.api.request('POST', url, headers=self.headers, json=filters)
        req.raise_for_status()
        return req.json()

    def get_measuregroup_elements_details(self, measure_id, filters=None):
        if type(filters) is fl.ComplexFilter or issubclass(type(filters), fl.SimpleFilter):
            filters = filters()
        elif filters is not None:
            raise AttributeError('Атрибут filters не является экземпляром наследника'
                                 ' класса SimpleFilter или экземпляром класса ComplexFilter')
        url = self.host + '/datacollection/api/measuregroups/%s/elements/details' % measure_id
        req = self.api.request('GET', url, headers=self.headers, json=filters)
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

        # Проверка что оба аргументы заданы или наоборот
        if (from_data is None or to_data is None) and from_data is not to_data:
            raise AttributeError('Необходимо задать агрументы from_data и to_data '
                                 'вместе или оба аргумента не задавать')

        # Вычисление второй даты, откуда брать инфу для переноса
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

        # Создание просто фильтров на дату
        past_filter = fl.ComplexFilter()
        cur_filter = fl.ComplexFilter()
        past_filter.add(fl.CalendarFilter(past_date))
        cur_filter.add(fl.CalendarFilter(cur_date))

        # Ищем, есть ли в заданном MEASUREGROUP указанный DIM
        template = self.get_measuregroup(group_id)
        dim_exist = False
        for i in template['dimensions'] + [template['measure']]:
            if i['id'] == dim:
                dim_exist = True

        # Если DIM не найден, то вызывать исключение
        if not dim_exist:
            raise AttributeError('Проверьте данные аргумента dim (ID группы показателей), '
                                 'они не найдёны в указанном описании текущего периода')

        # FROM_DATA и TO_DATA должны хранить в себе для поиска INT, поэтому мы ищем в узанном DIM
        # Сравниваем каждый элемент по имени и если совпадение найдено, то сохраняем его ID
        if type(from_data) == str or type(to_data) == str:
            for i in self.post_dimension_elements_search(dim)['elements']:
                if type(from_data) == str:
                    if i['name'].lower() == from_data.lower():
                        from_data = i['id']
                if type(to_data) == str:
                    if i['name'].lower() == to_data.lower():
                        to_data = i['id']

        # Если где-то замена на INT не прошла, значит вызываем исключние
        if type(from_data) == str or type(to_data) == str:
            raise AttributeError('Проверьте данные аргументов from_data и to_data, '
                                 'они не найдены в указанном описании текущего периода')

        # Определяем к чему отностится DIM, к dimensions
        if any(map(lambda x: x['id'] == dim, template['dimensions'])):
            if from_data is not None:
                past_filter.add(fl.DimensionIdFilter(from_data, dim))
                cur_filter.add(fl.DimensionIdFilter(to_data, dim))

        # Или относится к measure и задаём фильтр небходимый
        elif template['measure'] is not None:
            if template['measure']['id'] == dim:
                if from_data is not None:
                    past_filter.add(fl.MeasureIdFilter(from_data, dim))
                    cur_filter.add(fl.MeasureIdFilter(to_data, dim))

        # Получаем данные, и чистим то пространство, которое будем заполнять
        past_data = self.get_measuregroup_elements(group_id, past_filter)
        self.delete_measuregroup_elements(group_id, cur_filter)

        # Проходим по каждому элементу из полученных данных, парсим и приводим в нужный вид
        # Что бы задать эти данные там, где мы их удалили
        for elem in past_data['elements']:
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
                                'Date': cur_date.strftime('%Y-%m-%d')}]}])

    def get_measures_from_folder(self, dim):
        dimensions = self.get_dimensions()['dimensions']
        dims_list = list(filter(lambda x: x['id'] == dim or x['name'] == dim, dimensions))
        if dims_list:
            dim_id = dims_list[-1]['id']
        else:
            raise AttributeError('Проверьте dim, заданное значение не найдено')

        def subfolder(folder):
            children = self.get_dimension_folder_children(dim_id, folder['id'])['folders']
            if children:
                temp_dict = {}
                for a in children:
                    temp_dict.update(subfolder(a))
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

            # Добавление аттрибутов
            for attr in elem['attributes']:
                if 'linkedElementName' in attr:
                    attr_copy = attr.copy()
                    attr_copy.pop('attributeId')
                    data[attr['attributeId']] = attr_copy
                else:
                    data[attr['attributeId']] = attr['value']

            # Если это элемент подпапки в главной папке
            if elem['path']:
                temp = result[elem['path'][0]['folderName']]
                for fld in elem['path'][1:]:
                    temp = temp.get(fld['folderName'])
                # Если это самый глубокий уровень, в котором не папок
                if type(temp) is list:
                    temp.append(data)
                # Если уровень, в которое есть папки
                else:
                    temp['OTHERS'] = temp.get('OTHERS', [])
                    temp['OTHERS'].append(data)
            # Если элемент лежит в корне папки
            else:
                result['OTHERS'] = result.get('OTHERS', [])
                result['OTHERS'].append(data)
        # Если это папка без подпапок
        if not level_folders:
            return result['OTHERS']
        else:
            return result

    def get_measure_data_by_date(self, group_id, cur_date, dim,
                                 granularity='month', from_data=None):

        # Вычисление второй даты, откуда брать инфу для переноса
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

        # Создание просто фильтров на дату
        past_filter = fl.ComplexFilter()
        past_filter.add(fl.CalendarFilter(past_date))

        # Ищем, есть ли в заданном MEASUREGROUP указанный DIM
        template = self.get_measuregroup(group_id)
        dim_exist = False
        for i in template['dimensions'] + [template['measure']]:
            if i['id'] == dim:
                dim_exist = True

        # Если DIM не найден, то вызывать исключение
        if not dim_exist:
            raise AttributeError('Проверьте данные аргумента dim (ID группы показателей), '
                                 'они не найдёны в указанном описании текущего периода')

        # FROM_DATA должн хранить в себе для поиска INT, поэтому мы ищем в указанном DIM
        # Сравниваем каждый элемент по имени и если совпадение найдено, то сохраняем его ID
        if type(from_data) == str:
            for i in self.post_dimension_elements_search(dim)['elements']:
                if i['name'].lower() == from_data.lower():
                    from_data = i['id']
                    break

        # Если где-то замена на INT не прошла, значит вызываем исключние
        if type(from_data) == str:
            raise AttributeError('Проверьте данные аргументов from_data и to_data, '
                                 'они не найдены в указанном описании текущего периода')

        # Определяем к чему отностится DIM, к dimensions
        if any(map(lambda x: x['id'] == dim, template['dimensions'])):
            if from_data is not None:
                past_filter.add(fl.DimensionIdFilter(from_data, dim))

        # Или относится к measure и задаём фильтр небходимый
        elif template['measure'] is not None:
            if template['measure']['id'] == dim:
                if from_data is not None:
                    past_filter.add(fl.MeasureIdFilter(from_data, dim))

        # Получаем данные
        past_data = self.get_measuregroup_elements(group_id, past_filter)

        return past_data

    def get_n_elements(self, group_id, filters=None):
        # Получаем фильтр
        # Вытаскиваем из него все Атриьут фильтры и получаем все measure and dimensions и выбираем
        # те, у которых есть нужные нам атрибуты
        # Далее делаем норм фильтр
        # type(filters) is fl.ComplexFilter or issubclass(type(filters), fl.SimpleFilter)

        def generate_filter(comfilter):
            dimensions = self.get_measuregroup_elements_details(group_id)\
                ['measureGroup']['dimensions']
            dims_id = list(map(lambda x: x['id'], dimensions))
            result_comfil = fl.ComplexFilter()
            for dim in dims_id:
                try:
                    dims_elem = self.get_dimension_elements(dim, filters=comfilter)['elements']
                    for i in dims_elem:
                        result_comfil += fl.DimensionIdFilter(i['id'], dim)
                except exceptions.HTTPError:
                    pass
            return result_comfil

        if type(filters) is fl.ComplexFilter:
            dict_filters = filters()
            attr_filters = list(filter(lambda x: x['type'] == 'attribute', dict_filters['filters']))
            attr_comfil = fl.ComplexFilter()
            for elem in attr_filters:
                temp_filter = fl.DictFilter(elem)
                filters -= temp_filter
                attr_comfil += temp_filter
            filters.extend(generate_filter(attr_comfil))
        elif issubclass(type(filters), fl.SimpleFilter):
            comfil = fl.ComplexFilter()
            if type(filters) is fl.AttributeFilter:
                comfil += filters
                filters = generate_filter(comfil)
            else:
                comfil += filters
                filters = comfil
        elif filters is not None:
            raise AttributeError('Атрибут filters не является экземпляром наследника'
                                 ' класса SimpleFilter или экземпляром класса ComplexFilter')

        if not filters()['elements']:
            filters = None

        result = self.post_measuregroup_elements_search(group_id, filters=filters)
        return result

    @staticmethod
    def find_attribute_by_unique_name(dimension_element, attribute_unique_name):
        if type(dimension_element) is not dict or type(attribute_unique_name) is not str:
            raise AttributeError('Проверьте корректность введённых вами данных')
        for attribute in dimension_element['attributes']:
            if attribute['attributeId'] == attribute_unique_name:
                return attribute

    @staticmethod
    def find_dimension_element_by_predicate(dimension_elements, predicate):
        for element in dimension_elements['elements']:
            if predicate(element):
                return element

    @staticmethod
    def find_dimension_element_by_attribute(dimension_elements, attribute_unique_name,
                                            attribute_value):
        if type(dimension_elements) is not dict or type(attribute_unique_name) is not str:
            # or type(attribute_value) is not int:
            raise AttributeError('Проверьте корректность переданных вами данных')

        def predicate(element):
            attribute = DataCollection.find_attribute_by_unique_name(element, attribute_unique_name)
            return all((attribute is not None, attribute['value'] == attribute_value))

        return DataCollection.find_dimension_element_by_predicate(dimension_elements, predicate)

    @staticmethod
    def find_dimension_element_by_name(dimension_elements, element_name):
        if type(dimension_elements) is not dict or type(element_name) is not str:
            raise AttributeError('Проверьте корректность переданных вами данных')

        def predicate(element):
            return bool(element['name'] == element_name)

        return DataCollection.find_dimension_element_by_predicate(dimension_elements, predicate)

    @staticmethod
    def find_dimension_element_by_id(dimension_elements, element_id):
        if type(dimension_elements) is not dict or type(element_id) is not int:
            raise AttributeError('Проверьте корректность переданных вами данных')

        def predicate(element):
            return bool(element['id'] == element_id)

        return DataCollection.find_dimension_element_by_predicate(dimension_elements, predicate)

    @staticmethod
    def prepare_dimension_element_to_insert(dimension_element, attribute_map):
        if type(dimension_element) is not dict or type(attribute_map) is not dict:
            raise AttributeError('Проверьте корректность переданных вами данных')
        for attribute in dimension_element['attributes']:
            attribute_id = attribute['attributeId']
            if attribute_id in attribute_map:
                attribute['value'] = attribute_map[attribute_id]
        return dimension_element
