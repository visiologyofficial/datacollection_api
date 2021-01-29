from datetime import date


class SimpleFilter:
    json = {}
    ban_conditions = []

    def check_condition(self, condition):
        if condition not in self.ban_conditions:
            print(condition, self.ban_conditions, self.json)
        else:
            raise AttributeError('bad conditions')


class IdFilter(SimpleFilter):
    def __init__(self, value, condition='equals'):
        if type(value) is int:
            self.json = {'value': value,
                         'type': 'Id',
                         'condition': condition}
        else:
            raise AttributeError('Attribute value must be int type')

    def __call__(self):
        return self.json


class CalendarFilter(SimpleFilter):
    def __init__(self, value, condition='equals'):
        if type(value) is date:
            self.json = {'value': value.strftime('%Y-%m-%d'),
                         'type': 'calendar',
                         'condition': condition}
        else:
            raise AttributeError('Attribute value must be datetime.date object')

    def __call__(self):
        return self.json


class FormInstanceFilter(SimpleFilter):
    def __init__(self, value, condition='equals'):
        if type(value) is str:
            self.json = {'value': value,
                         'type': 'formInstance',
                         'condition': condition}
        else:
            raise AttributeError('Attribute value must be str type')

    def __call__(self):
        return self.json


class DimensionIdFilter(SimpleFilter):
    def __init__(self, value, name, condition='equals'):
        if type(value) is int:
            self.json = {'value': value,
                         'type': 'DimensionId',
                         'name': name,
                         'condition': condition}
        else:
            raise AttributeError('Attribute value and name must be int and str type')

    def __call__(self):
        return self.json


class DimensionNameFilter(SimpleFilter):
    def __init__(self, value, name, condition='equals'):
        self.ban_conditions = []
        if type(value) is str and type(name) is str:
            self.json = {'value': value,
                         'type': 'DimentionName',
                         'name': name,
                         'condition': condition}
        else:
            raise AttributeError('Attribute value and name must be str type')

    def __call__(self):
        return self.json


class MeasureIdFilter(SimpleFilter):
    def __init__(self, value, name, condition='equals'):
        if type(value) is int and type(name) is str:
            self.json = {'value': value,
                         'type': 'MeasureId',
                         'name': name,
                         'condition': condition}
        else:
            raise AttributeError('Attribute value and name must be int and str type')

    def __call__(self):
        return self.json


class MeasureNameFilter(SimpleFilter):
    def __init__(self, value, name, condition='equals'):
        if type(value) is str and type(name) is str:
            self.json = {'value': value,
                         'type': 'MeasureName',
                         'name': name,
                         'condition': condition}
        else:
            raise AttributeError('Attribute value and name must be str type')

    def __call__(self):
        return self.json


class ComplexFilter:
    def __init__(self, operation='and'):
        self.json = {'operation': operation, 'filters': []}

    def __call__(self):
        return self.json

    def __add__(self, other):
        self.add(other)
        return self

    def add(self, other):
        def add_element(element):
            if issubclass(type(element), SimpleFilter):
                self.json['filters'].append(element())
            else:
                raise AttributeError('не класс простых фильтров')

        if type(other) is list or type(other) is tuple:
            for i in other:
                add_element(i)
        else:
            add_element(other)

    def __sub__(self, other):
        self.remove(other)
        return self

    def remove(self, element):
        if type(element) is list or type(element) is tuple:
            for i in element:
                self.json['filters'].remove(i())
        else:
            self.json['filters'].remove(element())

    def set_operation(self, operation):
        self.json['operation'] = operation


comfil = ComplexFilter('or')
x = IdFilter(12, condition='notequals')
i = CalendarFilter(date(2020, 11, 28))
comfil = comfil + [x, x, i, i]
comfil += [FormInstanceFilter('form13213instance'), DimensionIdFilter(1, 'DimExample')]
comfil.add(DimensionNameFilter('DimNAME', 'DimExample'))
comfil.add([MeasureIdFilter(13, 'MeaExamp'), MeasureNameFilter('MeaName', 'MeaExamp')])
print(comfil())
comfil.set_operation('and')
comfil.remove([x, x])
comfil -= i
print(comfil())

# equals, notequals, greater, greaterorequals, less, lessorequals, contains
#    =       !=        >         >=              <        <=         in
