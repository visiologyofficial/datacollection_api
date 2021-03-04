## Документация по работе с фильтрами

В файле `filters.py` хранятся все необходимые классы для того, что бы задавать фильтры для функций __API__

### Простые фильтры

Все простые фильтры должны быть наследниками класса `SimpleFilter` 

---

#### `IdFilter` - _фильтрация по идентификатору элемента_
+ `value` - __ID__, по которому осуществлять фильтрацию
+ `condition='equals'` - условие фильтрации (equals, notequals, greater, greaterorequals, less, lessorequals)
```python
from filters import IdFilter

filter_id = IdFilter(1234, condition='notequals')
filter_id()
# {'value': 1234,
#  'type': 'Id',
#  'condition': 'notequals'}
```

#### `CalendarFilter` - _фильтрация по дате элемента_
+ `value` - __Date__, по которому осуществлять фильтрацию (передавать объектом `datetime.date`)
+ `condition='equals'` - условие фильтрации (equals, notequals, greater, greaterorequals, less, lessorequals)
```python
from filters import CalendarFilter
from datetime import date

filter_calendar = CalendarFilter(date(2020, 11, 28), condition='notequals')
filter_calendar()
# {'value': '2020-11-28'),
#  'type': 'calendar',
#  'condition': 'notequals'}
```

#### `FormInstanceFilter` - _фильтрация по идентификатору экземпляра формы_
+ `value` - __ID__ экземпляра формы, по которому осуществлять фильтрацию
+ `condition='equals'` - условие фильтрации (equals, notequals, greater, greaterorequals, less, lessorequals)
```python
from filters import FormInstanceFilter

filter_forminstance = FormInstanceFilter('ft12-d6f1-d7e1-d8e1-c2e1546300800000_Quarter', condition='notequals')
filter_forminstance()
# {'value': 'ft12-d6f1-d7e1-d8e1-c2e1546300800000_Quarter',
#  'type': 'formInstance',
#  'condition': 'notequals'}
```

#### `DimensionIdFilter` - _фильтрация по идентификатору Dimension_
+ `value` - __ID__ (идентификатор элемента) по которому осуществлять фильтрацию
+ `name` - __DimensionID__ 
+ `condition='equals'` - условие фильтрации (equals, notequals, greater, greaterorequals, less, lessorequals)
```python
from filters import DimensionIdFilter

filter_dimensionid = DimensionIdFilter(1234, 'dim_DimExample', condition='notequals')
filter_dimensionid()
# {'value': 1234,
#  'type': 'DimensionId',
#  'name': 'DimExample',
#  'condition': 'notequals'}
```

#### `DimensionNameFilter` - _фильтрация по имени Dimension_
+ `value` - __ID__ (идентификатор элемента) по которому осуществлять фильтрацию
+ `name` - __DimensionName__ 
+ `condition='equals'` - условие фильтрации (equals, notequals, greater, greaterorequals, less, lessorequals)
```python
from filters import DimensionNameFilter

filter_dimensionname = DimensionNameFilter(1234, 'Dim Пример', condition='notequals')
filter_dimensionname()
# {'value': 1234,
#  'type': 'DimensionName',
#  'name': 'Dim Пример',
#  'condition': 'notequals'}
```

#### `MeasureIdFilter` - _фильтрация по идентификатору Measure_
+ `value` - __ID__ (идентификатор элемента) по которому осуществлять фильтрацию
+ `name` - __MeasureID__ 
+ `condition='equals'` - условие фильтрации (equals, notequals, greater, greaterorequals, less, lessorequals)
```python
from filters import MeasureIdFilter

filter_measureid = MeasureIdFilter(1234, 'measure_MeaExample', condition='notequals')
filter_measureid()
# {'value': 1234,
#  'type': 'MeasureId',
#  'name': 'measure_MeaExample',
#  'condition': 'notequals'}
```

#### `MeasureNameFilter` - _фильтрация по имени Measure_
+ `value` - __ID__ (идентификатор элемента) по которому осуществлять фильтрацию
+ `name` - __MeasureID__ 
+ `condition='equals'` - условие фильтрации (equals, notequals, greater, greaterorequals, less, lessorequals)
```python
from filters import MeasureNameFilter

filter_measurename = MeasureNameFilter(1234, 'Mea Пример', condition='notequals')
filter_measurename()
# {'value': 1234,
#  'type': 'MeasureName',
#  'name': 'Mea Пример',
#  'condition': 'notequals'}
```

#### `AttributeFilter` - _фильтрация по атрибутам_
+ `value` - значение, по которому осуществлять фильтрацию
+ `name` - название атрибута (userfriendly)
```python
from filters import AttributeFilter

filter_attr = AttributeFilter('Примеров', 'Фамилия', condition='notequals')
filter_attr()
# {'value': 'Иванов', 
#  'name': 'Фамилия',
#  'type': 'attribute', 
#  'condition': 'equals'}
```

#### `DictFilter` - _фильтрация по вашему усмотрению_
Класс для тех, кто не хочет углубляться в использование простых фильтров
+ `value` - python-словарь (будет выступать в качестве фильтра при фильтр)
```python
from filters import DictFilter

slovar =  {'value': 1234, 'type': 'Id', 'condition': 'notequals'}

filter_dict = DictFilter(slovar)
filter_dict()
# {'value': 1234,
#  'type': 'Id',
#  'condition': 'notequals'}
# Обычно атрибуты имеются у dimensions
```

> Также вы можете создавать классы-фильтры с собственным поведение. Главным условием для создания такого класса является его наследование от класса `SimpleFilter`

---

### Комплексные фильтры

#### `ComplexFilter` - класс, для объединения классов простых фильтров
* `operation='and'` - логика объединения фильтров (or или and)
```python
from filters import *


comfil = ComplexFilter('or')
```

##### Добавление простых фильтров
Для добавления элементов в этот класс вы можете использовать функцию add(), а так же использовать оператор '+'.
При добавлении вы можете передавать как список классов-фильтров, так и сам класс-фильтр.

```python
spisok = [IdFilter(1000, condition='greater'), 
          IdFilter(2000, condition='less')]
comfil.add(spisok)
compfil.add(DimensionIdFilter(1, 'DimExample'))
```
```python
spisok = [IdFilter(1000, condition='greater'), 
          IdFilter(2000, condition='less')]
comfil += spisok
compfil += DimensionIdFilter(1, 'DimExample')
```

##### Удаление простых фильтров
Для удаления элементов в этом классе вы можете использовать функцию remove(), а так же использовать оператор '-'.
При удалении вы можете передавать как список классов-фильтров, так и сам класс-фильтр.

```python
spisok = [IdFilter(1000, condition='greater'), 
          IdFilter(2000, condition='less')]
comfil.remove(spisok)
compfil.remove(DimensionIdFilter(1, 'DimExample'))
```
```python
spisok = [IdFilter(1000, condition='greater'), 
          IdFilter(2000, condition='less')]
comfil -= spisok
compfil -= DimensionIdFilter(1, 'DimExample')
```
При удалении элемента из класса вам необязательно передавать именно тот экземпляр класса, который вы добавляли.
Вы можете передать другой экземпяр такого же класса простого фильтра, главное, что бы совпадали данные. Пример:
```python
comfil = ComplexFilter()

id_fil_1 = IdFilter(1000) # <filters.IdFilter object at 0x00000226615BC248>
comfil.add(id_fil_1)
comfil() 
# {'operation': 'and', 'filters': [ {'value': 1000, 'type': 'Id', 'condition': 'equals'} ]}

id_fil_2 = IdFilter(1000) # <filters.IdFilter object at 0x00000226615BC688>
comfil -= id_fil_2
comfil()
# {'operation': 'and', 'filters': []}
```

##### Объединение комплексных фильтров
Используя функцию extend() вы можете дополнить один комплексный фильтр данными из другого комплексного фильтра.
```python
comfil1 = ComplexFilter('or')
comfil1 += [FormInstanceFilter('form13213'), DimensionIdFilter(1, 'DimExample')]
print(comfil1())
# {'operation': 'or', 'filters': [{'value': 'form13213', 'type': 'formInstance', 'condition': 'equals'}, 
#                                 {'value': 1, 'type': 'DimensionId', 'name': 'DimExample', 'condition': 'equals'}]}

comfil2 = ComplexFilter('and')
comfil2 += [IdFilter(1234), MeasureIdFilter(13, 'MeaExamp')]
print(comfil2())
# {'operation': 'and', 'filters': [{'value': 1234, 'type': 'Id', 'condition': 'equals'}, 
#                                  {'value': 13, 'type': 'MeasureId', 'name': 'MeaExamp', 'condition': 'equals'}]}

comfil1.extend(comfil2)
print(comfil1())
# {'operation': 'or', 'filters': [{'value': 'form13213', 'type': 'formInstance', 'condition': 'equals'}, 
#                                 {'value': 1, 'type': 'DimensionId', 'name': 'DimExample', 'condition': 'equals'}, 
#                                 {'value': 1234, 'type': 'Id', 'condition': 'equals'}, 
#                                 {'value': 13, 'type': 'MeasureId', 'name': 'MeaExamp', 'condition': 'equals'}]}
```