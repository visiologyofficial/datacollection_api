import pytest
from datetime import date as ddate


def test_transfer_data(vdatacollection):
    current_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME,
                                                                {'operation': 'and', 'filters': [
                                                                {'value': pytest.PCURPER,
                                                                 'type': 'MeasureId',
                                                                 'name': pytest.DIMMEASUREGROUP,
                                                                 'condition': 'equals'},
                                                                {'value': pytest.CURDATE,
                                                                 'type': 'calendar',
                                                                 'condition': 'equals'}]})
    with pytest.raises(AttributeError):
        vdatacollection.transfer_data(pytest.MEASUREGROUPNAME, ddate(2020, 4, 1),
                                      pytest.DIMMEASUREGROUP, granularity='quarter',
                                      from_data=None, to_data=pytest.PCURPER)
    count = 0
    new_current_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME,
                                                                       {'operation': 'and', 'filters': [
                                                                        {'value': pytest.PCURPER,
                                                                            'type': 'MeasureId',
                                                                            'name': pytest.DIMMEASUREGROUP,
                                                                            'condition': 'equals'},
                                                                           {'value': pytest.CURDATE,
                                                                            'type': 'calendar',
                                                                            'condition': 'equals'}]})
    new_current_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    current_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    for i in range(len(current_period['elements'])):
        if new_current_period['elements'][i]['value'] == current_period['elements'][i]['value']:
            count += 1
    assert count == len(new_current_period['elements'])

    recent_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME, {'operation': 'and', 'filters': [
        {'value': pytest.PPASTPER,
         'type': 'MeasureId',
         'name': pytest.DIMMEASUREGROUP,
         'condition': 'equals'},
        {'value': pytest.RECDATE,
         'type': 'calendar',
         'condition': 'equals'}]})
    vdatacollection.transfer_data(pytest.MEASUREGROUPNAME, ddate(2020, 4, 1), pytest.DIMMEASUREGROUP, granularity = 'quarter',
                                  from_data=pytest.PPASTPER, to_data=pytest.PCURPER)
    current_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME, {'operation': 'and', 'filters': [
        {'value': pytest.PCURPER,
         'type': 'MeasureId',
         'name': pytest.DIMMEASUREGROUP,
         'condition': 'equals'},
        {'value': pytest.CURDATE,
         'type': 'calendar',
         'condition': 'equals'}]})
    count = 0
    recent_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    current_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    for i in range(len(recent_period['elements'])):
        if recent_period['elements'][i]['value'] == current_period['elements'][i]['value']:
            count += 1
    assert count == len(recent_period['elements'])

    recent_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME,
                                                                   {'operation': 'and', 'filters': [
                                                                       {'value': pytest.PPASTPER,
                                                                        'type': 'MeasureId',
                                                                        'name': pytest.DIMMEASUREGROUP,
                                                                        'condition': 'equals'},
                                                                       {'value': pytest.RECDATE,
                                                                        'type': 'calendar',
                                                                        'condition': 'equals'}]})
    vdatacollection.transfer_data(pytest.MEASUREGROUPNAME, ddate(2020, 4, 1), pytest.DIMMEASUREGROUP, granularity = 'quarter',
                                  from_data=pytest.PPASTPERSTR, to_data=pytest.PCURPERSTR)
    current_period = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME,
                                                                    {'operation': 'and', 'filters': [
                                                                        {'value': pytest.PCURPER,
                                                                         'type': 'MeasureId',
                                                                         'name': pytest.DIMMEASUREGROUP,
                                                                         'condition': 'equals'},
                                                                        {'value': pytest.CURDATE,
                                                                         'type': 'calendar',
                                                                         'condition': 'equals'}]})
    count = 0
    recent_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    current_period['elements'].sort(key=lambda x: x['dimensionElements'][1]['elementId'])
    for i in range(len(recent_period['elements'])):
        if recent_period['elements'][i]['value'] == current_period['elements'][i]['value']:
            count += 1
    assert count == len(recent_period['elements'])


def test_get_measuregroup_elements(vdatacollection):
    data = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME)
    assert type(data) is dict
    assert data


def test_post_dimension_by_uniquename(vdatacollection):
    data = vdatacollection.get_measuregroup_elements(pytest.MEASUREGROUPNAME)
    assert type(data) is dict
    assert data


def test_get_measures_from_folder(vdatacollection):
    result_1 = vdatacollection.get_measures_from_folder(pytest.DIMMEASUREGROUP)
    result_2 = vdatacollection.get_measures_from_folder(pytest.DIMMEASUREGROUPSTR, 'Активы')
    test_data_1 = [{'id': 1, 'name': 'Начало периода'},
                   {'id': 2, 'name': 'Изменение'},
                   {'id': 3, 'name': 'Конец периода'}]
    test_data_2 = {'Оборотные активы': [{'id': 3, 'name': 'Денежные средства'},
                                        {'id': 4, 'name': 'Дебиторская задолженность'},
                                        {'id': 5, 'name': 'Товары на складах'},
                                        {'id': 6, 'name': 'Всего оборотных активов'}],
                   'Внеоборотные активы': [{'id': 7, 'name': 'Основные средства'},
                                         {'id': 8, 'name': 'Всего внеоборотных активов'}]}
    assert result_1 == test_data_1
    assert result_2 == test_data_2

def test_get_measure_data_by_date(vdatacollection):
    data_for_test_1 = vdatacollection.get_measure_data_by_date(pytest.MEASUREGROUPNAME, ddate(2020, 7, 1), dim=pytest.DIMMEASUREGROUPSTR, granularity = 'quarter', from_data = 2)
    data_for_test_2 = vdatacollection.get_measure_data_by_date(pytest.MEASUREGROUPNAME, ddate(2020, 10, 1), dim=pytest.DIMMEASUREGROUPSTR, granularity = 'half year', from_data = 2)
    data_for_test_3 = vdatacollection.get_measure_data_by_date(pytest.MEASUREGROUPNAME, ddate(2020, 7, 1), dim=pytest.DIMMEASUREGROUPSTR, granularity = 'half year', from_data = 2)
    data_for_test_4 = vdatacollection.get_measure_data_by_date(pytest.MEASUREGROUPNAME, ddate(2020, 4, 1), dim=pytest.DIMMEASUREGROUPSTR, granularity='quarter',from_data=2)
    assert data_for_test_1 == data_for_test_2
    assert data_for_test_3 == data_for_test_4
    assert data_for_test_1 != data_for_test_3


def test_find_attribute_by_unique_name(vdatacollection):
    prediction = {'linkedElementName': None, 'attributeId': 'attr_Funktsiya_agregatsii', 'value': None}
    answer = vdatacollection.find_attribute_by_unique_name(vdatacollection.get_dimension_elements(pytest.DIMUTILS)['elements'][0], pytest.DIMUTILS_ATTR)
    assert prediction == answer

def test_find_dimension_element_by_attribute(vdatacollection):
    prediction = {'id': 1, 'name': 'Количество', 'path': [], 'attributes': [{'linkedElementName': None, 'attributeId': 'attr_Funktsiya_agregatsii', 'value': None}, {'linkedElementName': None, 'attributeId': 'attr_Edinitsa_izmereniya', 'value': None}, {'attributeId': 'attr_Kod_pokazatelya', 'value': None}, {'attributeId': 'attr_Tochnost_znakov_posle_', 'value': 0}]}
    answer = vdatacollection.find_dimension_element_by_attribute(vdatacollection.get_dimension_elements(pytest.DIMUTILS), "attr_Edinitsa_izmereniya", None)
    assert prediction == answer

def test_find_dimension_element_by_name(vdatacollection):
    prediction = {'id': 2, 'name': 'Цена', 'path': [], 'attributes': [{'linkedElementName': None, 'attributeId': 'attr_Funktsiya_agregatsii', 'value': None}, {'linkedElementName': None, 'attributeId': 'attr_Edinitsa_izmereniya', 'value': None}, {'attributeId': 'attr_Kod_pokazatelya', 'value': None}, {'attributeId': 'attr_Tochnost_znakov_posle_', 'value': 0}]}
    answer = vdatacollection.find_dimension_element_by_name(vdatacollection.get_dimension_elements(pytest.DIMUTILS), 'Цена')
    assert prediction == answer

def test_find_dimension_element_by_id(vdatacollection):
    prediction = {'id': 2, 'name': 'Цена', 'path': [], 'attributes': [{'linkedElementName': None, 'attributeId': 'attr_Funktsiya_agregatsii', 'value': None}, {'linkedElementName': None, 'attributeId': 'attr_Edinitsa_izmereniya', 'value': None}, {'attributeId': 'attr_Kod_pokazatelya', 'value': None}, {'attributeId': 'attr_Tochnost_znakov_posle_', 'value': 0}]}
    answer = vdatacollection.find_dimension_element_by_id(vdatacollection.get_dimension_elements(pytest.DIMUTILS), 2)
    assert prediction == answer

def test_prepare_dimension_element_to_insert(vdatacollection):
    prediction = {'id': 1, 'name': 'Количество', 'path': [], 'attributes': [{'linkedElementName': None, 'attributeId': 'attr_Funktsiya_agregatsii', 'value': 4}, {'linkedElementName': None, 'attributeId': 'attr_Edinitsa_izmereniya', 'value': None}, {'attributeId': 'attr_Kod_pokazatelya', 'value': 5}, {'attributeId': 'attr_Tochnost_znakov_posle_', 'value': 0}]}
    answer = vdatacollection.prepare_dimension_element_to_insert(vdatacollection.get_dimension_elements(pytest.DIMUTILS)['elements'][0], {"attr_Funktsiya_agregatsii": 4, "attr_Kod_pokazatelya": 5})
    assert prediction == answer