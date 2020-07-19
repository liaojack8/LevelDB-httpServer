# LevelDB-httpServer
RESTful API server based on leveldb storage engine

## Building
```
pip install -r requirements.txt
python3 server.py
```

## Options
```
    -db <str>       name of path to save leveldb file.
                    default: testdb
    -port <int>     the port which api using.
                    default: 8888
```

## API endpoints & request body:
http request body format: json
* /put
  

        {"key" : "<key>", "value" : "<value>"}
* /get

        {"key" : "<key>"}
* /delete
  
        {"key" : "<key>"}
* /query

    The key used here will be prefix to query data.

        {"key" : "<key>"}
* /queryall

        None

## Example
* put
```
curl -X POST 'http://127.0.0.1:8888/put' -H "Content-Type: application/json" -d '{"key" : "A", "value" : "Airplane"}'
```
```
Output:
        {
        "status": "OK"
        }
```
* get
```
curl -X GET 'http://127.0.0.1:8888/get' -H "Content-Type: application/json" -d '{"key" : "A"}'
```
```
Output:
        {
        "data": "(A, Airplane)",
        "status": "OK"
        }
```
* delete
```
curl -X POST 'http://127.0.0.1:8888/delete' -H "Content-Type: application/json" -d '{"key" : "A"}'
```
```
Output:
        {
        "status": "OK"
        }
```
* query & queryall
  
```
curl -X POST 'http://127.0.0.1:8888/put' -H "Content-Type: application/json" -d '{"key" : "k1", "value" : "foo1"}'
curl -X POST 'http://127.0.0.1:8888/put' -H "Content-Type: application/json" -d '{"key" : "k2", "value" : "foo2"}'

curl -X POST 'http://127.0.0.1:8888/put' -H "Content-Type: application/json" -d '{"key" : "A1", "value" : "Airplane1"}'
curl -X POST 'http://127.0.0.1:8888/put' -H "Content-Type: application/json" -d '{"key" : "A2", "value" : "Airplane2"}'
curl -X POST 'http://127.0.0.1:8888/put' -H "Content-Type: application/json" -d '{"key" : "A3", "value" : "Airplane3"}'
curl -X POST 'http://127.0.0.1:8888/put' -H "Content-Type: application/json" -d '{"key" : "A4", "value" : "Airplane4"}'
```

```
Output: Omit
```

```
curl -X GET 'http://127.0.0.1:8888/queryall'
```
```
Output: 
        {
        "data": [
        "(A1, Airplane1)",
        "(A2, Airplane2)",
        "(A3, Airplane3)",
        "(A4, Airplane4)",
        "(k1, foo1)",
        "(k2, foo2)"
        ],
        "status": "OK"
        }
```
```
curl -X GET 'http://127.0.0.1:8888/query' -H "Content-Type: application/json" -d '{"key" : "k"}'
```
```
Output: 
        {
        "data": [
        "(k1,foo1)",
        "(k2,foo2)"
        ],
        "status": "OK"
        }
```