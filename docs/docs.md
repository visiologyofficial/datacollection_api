# DataCollection for python3

Библиотека позволяет обращаться к DataCollection API v2.0 при помощи объектно-ориентированной модели python3.

## Установка пакетов

Для удовлетворения зависимостей, воспользуйтесь командой:

```bash
pip3 install -r requirements.txt
```

## Инициализация

Создадим объект-обёртку API - **DataCollection**

```python
api_host = 'http://84.201.138.2'
dc = DataCollection(api_host)
```

## Авторизация

Библиотека предусматривает авторизацию как по данным учётной записи, так и по токену, если он уже известен.

```python
dc.auth_by_username(login, password)  # by login & password
dc.auth_by_token(token_type, access_token)  # by token
```

## Методы API

Атрибут `filters` необходимо передавать как экземпляр класс `ComplexFilter` или как экземпляр наследника класса `SimpleFilter`

##### `dc.get_dimension_attributes(dim_id, filters=None)`
Возвращает атрибуты измерений по его __ID__ в формате python-словаря.

##### `dc.get_dimension_elements(dim_id, filters=None)`
Возвращает элементы и описание измерения по его __ID__ в формате python-словаря.

##### `dc.put_dimension_elements(dim_id, data=None, filters=None)`
Обновляет элементы измерения по его __ID__. В `data` передаются в формате python-словаря будущие данные.

##### `dc.post_dimension_elements(dim_id, data=None)`
Создаёт элементы измерения по его __ID__. В `data` передаются данные в формате python-словаря, которые будут созданы.

##### `dc.delete_dimension_elements(dim_id, filters=None)`
Удаляет элементы измерения по его __ID__.

##### `dc.post_dimension_elements_search(dim_id, filters=None)`
Возвращает элементы измерения и описание измерения по его __ID__ в формате python-словаря.

##### `dc.get_dimension_folders(dim_id)`
Возвращает каталоги измерения по его __ID__ в формате python-словаря.

##### `dc.get_dimension_folder_children(dim_id, folder_id)`
Возвращает каталоги измерения, которые являются дочерними каталогами указанного каталога измерения по его __ID__ в формате python-словаря.

##### `dc.get_dimension_level_folders(dim_id, level_id)`
Возвращает каталоги измерения, которые находятся на указанном уровне измерения по его __ID__ в формате python-словаря.

##### `dc.get_dimension_levels(dim_id)`
Возвращает уровни измерения по его __ID__ в формате python-словаря.

##### `dc.get_dimensions()`
Возвращает описание всех измерений в формате python-словаря.

##### `dc.get_measuregroup_elements(measure_id, filters=None)`
Возвращает элементы с описанием группы показателей по его __ID__ в формате python-словаря.

##### `dc.post_measuregroup_elements(measure_id, data=None)`
Создаёт элементы группы показателей по его __ID__. В `data` передаются данные в формате python-словаря, которые будут созданы.

##### `dc.delete_measuregroup_elements(measure_id, filters=None)`
Удалить элементы группы показателей по его __ID__.

##### `dc.get_measuregroup(measure_id)`
Возвращает описание группы показателей по его __ID__ в формате python-словаря.

##### `dc.get_measuregroups()`
Возвращает список групп показателей в формате python-словаря.

#### Специальные методы

##### `dc.transfer_data(group_id, cur_date, dim, granularity='month', from_data=None, to_data=None)`
Осуществляет заполнение ячеек эквивалентным значением из прошлого отчетного периода с
изменением одной координаты
+ `group_id` - описание текущего периода
+ `cur_date` - текущая дата с учетом гранулярности (передавать объектом `datetime.date`)
+ `dim` - ID группы показателей
+ `granularity` - гранулярность периодичности (day, week, month, quarter, half year, year)
+ `from_data` - показатель текущего периода (аргумент обязятельно именнованный)
+ `to_data` - показатель прошлого периода (аргумент обязятельно именнованный)

##### `dc.get_measure_data_by_date(group_id, cur_date, dim, granularity='month', from_data=None)`
Возвращает эквивалентное значение из прошлого периода без изменения координаты
+ `group_id` - описание текущего периода
+ `cur_date` - текущая дата с учетом гранулярности (передавать объектом `datetime.date`)
+ `dim` - ID группы показателей
+ `granularity` - гранулярность периодичности (day, week, month, quarter, half year, year)
+ `from_data` - показатель текущего периода (аргумент обязятельно именнованный)

##### `dc.get_measures_from_folder(dim)`
Возвращает все элементы измерений из папки
+ `dim` - __ID__ папки (пример: Mediastore. Продукты / dim_Produkti)

##### `dc.get_n_elements(group_id, filters=None)`
Получение всех элементов, кроме N элементов
+ `group_id` - __ID__ группы показателей
+ `filters` - фильтры
> Получаемые данные можно полностью отфильтровать с помощью фильтров 

##### `dc.find_attribute_by_unique_name(dimension_element, attribute_unique_name)`
Возвращает атрибуты элемента измерения`

##### `dc.find_dimension_element_by_predicate(dimension_elements, predicate)`
Возвращает элемент измерения по передаваемой функции

##### `dc.find_dimension_element_by_attribute(dimension_elements, attribute_unique_name, attribute_value)`
Возвращает элемент измерения по атрибутам

##### `dc.find_dimension_element_by_name(dimension_elements, element_name)`
Возаращает элемент измерения по имени

##### `dc.find_dimension_element_by_id(dimension_elements, element_id)`
Возвращает элемент измерения по `id`

##### `dc.prepare_dimension_element_to_insert(dimension_element, attribute_map)`
Изменяет значение `value` в элементе измерения 

## Обработка ошибок
Методы библиотеки предусматривают вызов python-исключений в случае возникновения ошибки на стороне API.
+ `HTTPError`, если API возвращает код ошибки (404, 400, 500...)
+ `AttributeError`, если 
    * в функцию `dc.transfer_data` передан только один аргумент из аргументов `from_data` и `to_data`
    * в функцию `dc.transfer_data` передан неверно аргумент `granularity` 
    * в функцию `dc.transfer_data` передан аргумент `dim` (ID группы показателей), которого нет в описании текущего периода
    * в функцию `dc.transfer_data` передан один или оба аргумента `from_data` и `to_data` не найдены в описании текущего периода
    * в функцию `dc.get_measures_from_folder` передан аргумент `dim` (ID группы показателей), которого не существует
    * в функцию `dc.get_measure_data_by_date` передан неверно аргумент `granularity` 
    * в функцию `dc.get_measure_data_by_date` передан аргумент `dim` (ID группы показателей), которого нет в описании текущего периода
    * в функцию `dc.get_measure_data_by_date` передан один или оба аргумента `from_data` и `to_data` не найдены в описании текущего периода
    * в функцию `dc.find_attribute_by_unique_name` некорректно переданы данные
    * в функцию `dc.find_dimension_element_by_attribute` некорректно переданы данные
    * в функцию `dc.find_dimension_element_by_name` некорректно переданы данные
    * в функцию `dc.find_dimension_element_by_id` некорректно переданы данные
    * в функцию `dc.prepare_dimension_element_to_insert` некорректно переданы данные
    
