from datetime import date


class SimpleFilter:
    pass


class IdFilter(SimpleFilter):
    def __init__(self, value, condition='equals'):
        if condition not in ['equals', 'notequals', 'greater',
                             'greaterorequals', 'less', 'lessorequals']:
            raise AttributeError('Атрибут condition неверный')
        elif type(value) is int:
            self.json = {'value': value,
                         'type': 'Id',
                         'condition': condition}
        else:
            raise AttributeError('Атрибут value должен быть типа int')

    def __call__(self):
        return self.json


class CalendarFilter(SimpleFilter):
    def __init__(self, value, condition='equals'):
        if condition not in ['equals', 'notequals', 'greater',
                             'greaterorequals', 'less', 'lessorequals']:
            raise AttributeError('Атрибут condition неверный')
        elif type(value) is date:
            self.json = {'value': value.strftime('%Y-%m-%d'),
                         'type': 'calendar',
                         'condition': condition}
        else:
            raise AttributeError('Атрибут value должен быть объектом datetime.date')

    def __call__(self):
        return self.json


class FormInstanceFilter(SimpleFilter):
    def __init__(self, value, condition='equals'):
        if condition not in ['equals', 'notequals', 'greater',
                             'greaterorequals', 'less', 'lessorequals']:
            raise AttributeError('Атрибут condition неверный')
        elif type(value) is str:
            self.json = {'value': value,
                         'type': 'formInstance',
                         'condition': condition}
        else:
            raise AttributeError('Атрибут value должен быть типа str')

    def __call__(self):
        return self.json


class DimensionIdFilter(SimpleFilter):
    def __init__(self, value, name, condition='equals'):
        if condition not in ['equals', 'notequals', 'greater',
                             'greaterorequals', 'less', 'lessorequals']:
            raise AttributeError('Атрибут condition неверный')
        elif type(value) is int and type(name) is str:
            self.json = {'value': value,
                         'type': 'DimensionId',
                         'name': name,
                         'condition': condition}
        else:
            raise AttributeError('Атрибуты value и name должны быть типа int и str соответственно')

    def __call__(self):
        return self.json


class DimensionNameFilter(SimpleFilter):
    def __init__(self, value, name, condition='equals'):
        if condition not in ['equals', 'notequals', 'greater',
                             'greaterorequals', 'less', 'lessorequals']:
            raise AttributeError('Атрибут condition неверный')
        elif type(value) is int and type(name) is str:
            self.json = {'value': value,
                         'type': 'DimensionName',
                         'name': name,
                         'condition': condition}
        else:
            raise AttributeError('Атрибуты value и name должны быть типа int и str соответственно')

    def __call__(self):
        return self.json


class MeasureIdFilter(SimpleFilter):
    def __init__(self, value, name, condition='equals'):
        if condition not in ['equals', 'notequals', 'greater',
                             'greaterorequals', 'less', 'lessorequals']:
            raise AttributeError('Атрибут condition неверный')
        elif type(value) is int and type(name) is str:
            self.json = {'value': value,
                         'type': 'MeasureId',
                         'name': name,
                         'condition': condition}
        else:
            raise AttributeError('Атрибуты value и name должны быть типа int и str соответственно')

    def __call__(self):
        return self.json


class MeasureNameFilter(SimpleFilter):
    def __init__(self, value, name, condition='equals'):
        if condition not in ['equals', 'notequals', 'greater',
                             'greaterorequals', 'less', 'lessorequals']:
            raise AttributeError('Атрибут condition неверный')
        elif type(value) is str and type(name) is str:
            self.json = {'value': value,
                         'type': 'MeasureName',
                         'name': name,
                         'condition': condition}
        else:
            raise AttributeError('Атрибуты value и name должны быть типа str')

    def __call__(self):
        return self.json


class AttributeFilter(SimpleFilter):
    def __init__(self, value, name, condition='equals'):
        if condition not in ['equals', 'notequals']:
            raise AttributeError('Атрибут condition неверный')
        self.json = {'value': value,
                     'name': name,
                     'type': 'attribute',
                     'condition': condition}

    def __call__(self):
        return self.json


class DictFilter(SimpleFilter):
    def __init__(self, value):
        self.json = value

    def __call__(self):
        return self.json


class ComplexFilter:
    def __init__(self, operation='and'):
        if operation not in ['or', 'and']:
            AttributeError('Operation должен быть "or" или "and"')
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
                raise AttributeError('Элемент не является наследником класса SimpleFilter')

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
        if operation == 'or' or operation == 'and':
            self.json['operation'] = operation
        else:
            AttributeError('Operation должен быть "or" или "and"')

    def extend(self, complex_filter):
        if type(complex_filter) is not ComplexFilter:
            raise AttributeError('complex_filter должен быть экземпляром класса ComplexFilter')
        else:
            self.json['filters'].extend(complex_filter()['filters'])


'''
# Пример использование комплексного фильтра
comfil = ComplexFilter('or')

id_fil = IdFilter(1234, condition='notequals')
cal_fil = CalendarFilter(date(2020, 11, 28))

comfil = comfil + [id_fil, id_fil, cal_fil, cal_fil]
comfil += [FormInstanceFilter('form13213instance'), DimensionIdFilter(1, 'DimExample')]

comfil.add(DimensionNameFilter('DimNAME', 'DimExample'))
comfil.add([MeasureIdFilter(13, 'MeaExamp'), MeasureNameFilter('MeaName', 'MeaExamp')])

print(comfil())

comfil.set_operation('and')
comfil.remove([id_fil, IdFilter(1234, condition='notequals')])
comfil -= cal_fil

print(comfil())
'''
# equals, notequals, greater, greaterorequals, less, lessorequals, contains
#    =        !=        >            >=         <          <=         in
