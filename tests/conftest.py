import pytest
import os, sys
from datetime import date


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import *

""" TEST CONSTANTS """

HOST = 'http://84.201.138.2'
USERNAME = 'Admin'
PASSWORD = 'cwndQd9Bk7JVdnW'
MEASUREGROUPNAME = 'measureGroup_Byudzhet_po_balan'
DIMMEASUREGROUP = 'dim_Pokazateli_byudzheta_po_ba'
DIMMEASUREGROUPSTR = 'dim_Stati_byudzheta_po_balanso'
CURDATE = date(2020, 4, 1)
RECDATE = date(2020, 1, 1)
PCURPER = 1
PPASTPER = 3
STRCOUNT = 3
PCURPERSTR = "НачаЛо пеРиода"
PPASTPERSTR = "КоНец периОда"
DIMUTILS = 'dim_Plan_prodazh'
DIMUTILS_ATTR = "attr_Funktsiya_agregatsii"
# PLEASE FILL IT WITH SOME DATA FOR TESTING

""" -------------- """


@pytest.fixture(scope='module')
def vdatacollection_without_auth():
    pytest.USERNAME = USERNAME
    pytest.PASSWORD = PASSWORD
    yield DataCollection(HOST)


@pytest.fixture(scope='module')
def vdatacollection():
    pytest.USERNAME = USERNAME
    pytest.PASSWORD = PASSWORD
    pytest.MEASUREGROUPNAME = MEASUREGROUPNAME
    pytest.DIMMEASUREGROUP = DIMMEASUREGROUP
    pytest.DIMMEASUREGROUPSTR = DIMMEASUREGROUPSTR
    pytest.CURDATE = CURDATE
    pytest.RECDATE = RECDATE
    pytest.PCURPER = PCURPER
    pytest.PPASTPER = PPASTPER
    pytest.STRCOUNT = STRCOUNT
    pytest.PCURPERSTR = PCURPERSTR
    pytest.PPASTPERSTR = PPASTPERSTR
    pytest.DIMUTILS = DIMUTILS
    pytest.DIMUTILS_ATTR = DIMUTILS_ATTR
    obj = DataCollection(HOST)
    obj.auth_by_username(USERNAME, PASSWORD)
    yield obj
