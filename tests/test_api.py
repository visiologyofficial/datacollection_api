import pytest
from requests import HTTPError
from filters import *


def test_transfer_data(vdatacollection):
    comfil1 = ComplexFilter()
    comfil1 += [MeasureIdFilter(pytest.PCURPER, pytest.DIMMEASUREGROUP),
                CalendarFilter(pytest.CURDATE)]
    current_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME, comfil1)

    with pytest.raises(AttributeError):
        vdatacollection.transfer_data(pytest.MEASUREGROUPNAME, date(2020, 4, 1),
                                      pytest.DIMMEASUREGROUP, granularity='quarter',
                                      from_data=None, to_data=pytest.PCURPER)
    count = 0
    comfil2 = ComplexFilter()
    comfil2 += [MeasureIdFilter(pytest.PCURPER, pytest.DIMMEASUREGROUP),
                CalendarFilter(pytest.CURDATE)]
    new_current_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME, comfil2)

    new_current_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    current_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    for i in range(len(current_period['elements'])):
        if new_current_period['elements'][i]['value'] == current_period['elements'][i]['value']:
            count += 1
    assert count == len(new_current_period['elements'])

    comfil3 = ComplexFilter()
    comfil3 += [MeasureIdFilter(pytest.PPASTPER, pytest.DIMMEASUREGROUP),
                CalendarFilter(pytest.RECDATE)]

    recent_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME, comfil3)
    vdatacollection.transfer_data(pytest.MEASUREGROUPNAME, date(2020, 4, 1),
                                  pytest.DIMMEASUREGROUP, granularity='quarter',
                                  from_data=pytest.PPASTPER, to_data=pytest.PCURPER)

    comfil4 = ComplexFilter()
    comfil4 += [MeasureIdFilter(pytest.PCURPER, pytest.DIMMEASUREGROUP),
                CalendarFilter(pytest.CURDATE)]
    current_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME, comfil4)
    count = 0
    recent_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    current_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    for i in range(len(recent_period['elements'])):
        if recent_period['elements'][i]['value'] == current_period['elements'][i]['value']:
            count += 1
    assert count == len(recent_period['elements'])

    comfil5 = ComplexFilter()
    comfil5 += [MeasureIdFilter(pytest.PPASTPER, pytest.DIMMEASUREGROUP),
                CalendarFilter(pytest.RECDATE)]
    recent_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME, comfil5)
    vdatacollection.transfer_data(pytest.MEASUREGROUPNAME, date(2020, 4, 1),
                                  pytest.DIMMEASUREGROUP, granularity='quarter',
                                  from_data=pytest.PPASTPERSTR, to_data=pytest.PCURPERSTR)

    comfil6 = ComplexFilter()
    comfil6 += [MeasureIdFilter(pytest.PCURPER, pytest.DIMMEASUREGROUP),
                CalendarFilter(pytest.CURDATE)]
    current_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME, comfil6)
    count = 0
    recent_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    current_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    for i in range(len(recent_period['elements'])):
        if recent_period['elements'][i]['value'] == current_period['elements'][i]['value']:
            count += 1
    assert count == len(recent_period['elements'])


def test_get_measuregroup_elements(vdatacollection):
    vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME)
    with pytest.raises(HTTPError):
        vdatacollection.get_measuregroup_elements('fieghuheig')


def test_post_dimension_by_uniquename(vdatacollection):
    data = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME)
    assert type(data) is dict
    assert data
    with pytest.raises(HTTPError):
        vdatacollection.get_measuregroup_elements(542578)


def test_get_measures_from_folder(vdatacollection):
    result_1 = vdatacollection.get_measures_from_folder(pytest.DIMMEASUREGROUP)
    result_2 = vdatacollection.get_measures_from_folder(pytest.DIMMEASUREGROUPSTR, 'Активы')
    test_data_1 = [{'id': 1, 'name': 'Начало периода', 'attr_Tochnost_znakov_posle_': None,
                    'attr_Funktsiya_agregatsii': {'linkedElementName': None, 'value': None},
                    'attr_Edinitsa_izmereniya': {'linkedElementName': None, 'value': None},
                    'attr_Kod_pokazatelya': None},
                   {'id': 2, 'name': 'Изменение', 'attr_Tochnost_znakov_posle_': None,
                    'attr_Funktsiya_agregatsii': {'linkedElementName': None, 'value': None},
                    'attr_Edinitsa_izmereniya': {'linkedElementName': None, 'value': None},
                    'attr_Kod_pokazatelya': None},
                   {'id': 3, 'name': 'Конец периода', 'attr_Tochnost_znakov_posle_': None,
                    'attr_Funktsiya_agregatsii': {'linkedElementName': None, 'value': None},
                    'attr_Edinitsa_izmereniya': {'linkedElementName': None, 'value': None},
                    'attr_Kod_pokazatelya': None}]
    test_data_2 = {'Активы': {'Оборотные активы': [],
                              'Внеоборотные активы': []},
                   'Обязательства': {'Краткосрочные обязательства': [],
                                     'Долгосрочные обязательства': []},
                   'Капитал и резервы': []}

    assert result_1 == test_data_1
    assert result_2 == test_data_2
    with pytest.raises(AttributeError):
        vdatacollection.get_measures_from_folder('geuohgoeg')


def test_get_n_elements(vdatacollection):
    test_filters = ComplexFilter()
    test_filters += [AttributeFilter('Иванов', 'Фамилия'), CalendarFilter(date(2020, 1, 1)),
                     MeasureIdFilter(4, 'dim_Plan_prodazh'), IdFilter(5981, condition='greater')]
    test_data ={'elements': [{'dimensionElements': [{'dimensionId': 'dim_Filiali', 'elementId': 1},
                                                    {'dimensionId': 'dim_Produkti', 'elementId': 7},
                                                    {'dimensionId': 'dim_Versii', 'elementId': 1},
                                                    {'dimensionId': 'dim_Mediastore_Menedzhery',
                                                     'elementId': 1}],
                              'measureElements': [{'measureId': 'dim_Plan_prodazh', 'elementId': 4}],
                              'calendar': {'dateWithGranularity': '1 квартал',
                                           'date': '2020-01-01T00:00:00Z',
                                           'granularity': 'Квартал'}, 'attributes': [], 'id': 6017,
                              'value': 74.0, 'comment': None, 'systemInfo': None}],
                'measureGroup': {'name': 'Mediastore. План продаж',
                                 'id': 'measureGroup_Plan_prodazh',
                                 'dimensions': [{'name': 'Mediastore. Филиалы',
                                                 'id': 'dim_Filiali'},
                                                {'name': 'Mediastore. Продукты',
                                                 'id': 'dim_Produkti'},
                                                {'name': 'Mediastore. Версии', 'id': 'dim_Versii'},
                                                {'name': 'Mediastore. Менеджеры',
                                                 'id': 'dim_Mediastore_Menedzhery'}],
                                 'measure': {'name': 'Mediastore. Плановые показатели продаж',
                                             'id': 'dim_Plan_prodazh'},
                                 'calendar': {'name': 'Календарь', 'id': 'cal_Kvartal'},
                                 'attributes': []}}
    req = vdatacollection.get_n_elements('measureGroup_Plan_prodazh', filters=test_filters)
    assert test_data == req
    with pytest.raises(AttributeError):
        vdatacollection.get_measuregroup_elements('measureGroup_Plan_prodazh',
                                                  filters={1: 'тест что кидает ошибку на фильтр'})
