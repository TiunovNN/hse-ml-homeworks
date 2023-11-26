import csv
import io
import logging
from http import HTTPStatus

from fastapi.testclient import TestClient

from api import app

client = TestClient(app)
logging.basicConfig(level=logging.DEBUG)


def test_predict_item():
    response = client.post(
        '/predict_item',
        json={
            'name': 'Volkswagen Jetta',
            'year': 2020,
            'km_driven': 60000,
            'fuel': 'Petrol',
            'seller_type': 'Individual',
            'transmission': 'Manual',
            'owner': 'First Owner',
            'mileage': '17.0 kmpl',
            'engine': '1600 CC',
            'max_power': '80 bhp',
            'torque': '90Nm@ 3500rpm',
            'seats': 5.0,
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert float(response.content) > 0


csv_data = """
name,year,km_driven,fuel,seller_type,transmission,owner,mileage,engine,max_power,torque,seats
Mahindra Xylo E4 BS IV,2010,168000,Diesel,Individual,Manual,First Owner,14.0 kmpl,2498 CC,112 bhp,260 Nm at 1800-2200 rpm,7.0
BMW X4 M Sport X xDrive20d,2019,8500,Diesel,Dealer,Automatic,First Owner,16.78 kmpl,1995 CC,190 bhp,400Nm@ 1750-2500rpm,5.0
Ambassador Grand 1500 DSZ BSIII,2008,60000,Diesel,Individual,Manual,Second Owner,12.8 kmpl,1995 CC,52 bhp,106Nm@ 2200rpm,5.0
Mahindra Xylo D4 BSIII,2013,300000,Diesel,Individual,Manual,First Owner,14.0 kmpl,2498 CC,112 bhp,260 Nm at 1800-2200 rpm,8.0
"""

expected_result = [
    646789,
    1986911,
    56983,
    677191,
]


def test_predict_items():
    response = client.post('/predict_items', files={'file': csv_data})
    assert response.status_code == HTTPStatus.OK
    reader = csv.DictReader(io.StringIO(response.text), dialect='unix')
    assert expected_result == [
        int(float(row['selling_price']))
        for row in reader
    ], response.text
