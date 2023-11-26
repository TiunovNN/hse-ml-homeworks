# Домашнее задание №1

## Файлы

* [jupyter-ноутбук](HW1_Regression_with_inference.ipynb)
* [Код API](api.py)
* [Unit-тесты на API](tests/test_api.py)

## Выводы

Во время выполнения ДЗ было:
1. проанализирован датасет с продажами автомобилей;
2. выполнена нормализация данных, в том числе категориальных признаков;
3. построены графики, для обзорного анализа данных
4. обучены модели разными способами:
   * без регуляризации
   * с регуляризацией
   * с поиском оптимальных гиперпараметров через GridSearch
5. Написано API для предсказания стоимости автомобилей на основе признаков.

## API

### Запуск тестов

В директории `homework1`
```shell
$ pytest .
```

### Ответ API

```shell
$ curl -v -XPOST 'http://0.0.0.0:80/predict_items' -F 'file=@test.csv'
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 0.0.0.0:80...
* Connected to 0.0.0.0 (127.0.0.1) port 80 (#0)
> POST /predict_items HTTP/1.1
> Host: 0.0.0.0
> User-Agent: curl/7.88.1
> Accept: */*
> Content-Length: 795
> Content-Type: multipart/form-data; boundary=------------------------f634688c2b44d823
> 
* We are completely uploaded and fine
< HTTP/1.1 200 OK
< date: Sun, 26 Nov 2023 12:59:26 GMT
< server: uvicorn
< content-disposition: attachment; filename="result.csv"
< Transfer-Encoding: chunked
< 
name,year,km_driven,fuel,seller_type,transmission,owner,mileage,engine,max_power,torque,seats,selling_price
Mahindra Xylo E4 BS IV,2010,168000,Diesel,Individual,Manual,First Owner,14.0,2498.0,112.0,260 Nm at 1800-2200 rpm,7.0,646789.8847199891
BMW X4 M Sport X xDrive20d,2019,8500,Diesel,Dealer,Automatic,First Owner,16.78,1995.0,190.0,400Nm@ 1750-2500rpm,5.0,1986911.6605103235
Ambassador Grand 1500 DSZ BSIII,2008,60000,Diesel,Individual,Manual,Second Owner,12.8,1995.0,52.0,106Nm@ 2200rpm,5.0,56983.11008938536
Mahindra Xylo D4 BSIII,2013,300000,Diesel,Individual,Manual,First Owner,14.0,2498.0,112.0,260 Nm at 1800-2200 rpm,8.0,677191.1470006033
```

```shell
$ curl -v  -X 'POST' \
  'http://0.0.0.0/predict_item' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Volkswagen Jetta",
    "year": 2020,
    "km_driven": 60000,
    "fuel": "Petrol",
    "seller_type": "Individual",
    "transmission": "Manual",
    "owner": "First Owner",
    "mileage": "17.0 kmpl",
    "engine": "1600 CC",
    "max_power": "80 bhp",
    "torque": "90Nm@ 3500rpm",
    "seats": 5.0
}'

*   Trying 0.0.0.0:80...
* Connected to 0.0.0.0 (127.0.0.1) port 80 (#0)
> POST /predict_item HTTP/1.1
> Host: 0.0.0.0
> User-Agent: curl/7.88.1
> accept: application/json
> Content-Type: application/json
> Content-Length: 318
> 
< HTTP/1.1 200 OK
< date: Sun, 26 Nov 2023 13:00:28 GMT
< server: uvicorn
< content-length: 17
< content-type: application/json
< 
* Connection #0 to host 0.0.0.0 left intact
628789.6347232484%                
```
