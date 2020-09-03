# LevelDB-httpServer
A RESTful API server supports YCSB, and based on leveldb storage engine.
## Changelog
* 2020-09-03

Add `getProperty` API endpoint to close db completely.

* 2020-08-25

Add `shutdown` API endpoint to close db completely.

* 2020-07-20

Try to be compatible with YCSB (maybe not fully).

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
                    default: 8080
```

## API endpoints & request body:
* /put

        key=<key>
        value=<value>
* /get

        key=<key>
* /delete
  
        key=<key>
* /query

    The key used here will be prefix to query data.

        key=<key>
* /queryall

        None
* /shutdown

        None
* /getProperty

        name=<property name>

## Example
* put
```bash
$ curl -X POST 'http://127.0.0.1:8080/put?key=A&value=Airplane'
```
```
Output:
        {
        "status_txt": "OK",
        "status_code": 200,
        "data": ""
        }
```
* get
```bash
$ curl -X GET 'http://127.0.0.1:8080/get?key=A'
```
```
Output:
        {
        "status_txt": "OK",
        "status_code": 200,
        "data": "Airplane"
        }
```
* delete
```bash
$ curl -X POST 'http://127.0.0.1:8080/delete?key=A'
```
```bash
Output:
        {
        "status_txt": "OK",
        "status_code": 200,
        "data": ""
        }
```
* query & queryall
  
```bash
$ curl -X POST 'http://127.0.0.1:8080/put?key=k1&value=foo1'
$ curl -X POST 'http://127.0.0.1:8080/put?key=k2&value=foo2'

$ curl -X POST 'http://127.0.0.1:8080/put?key=A1&value=Airplane1'
$ curl -X POST 'http://127.0.0.1:8080/put?key=A2&value=Airplane2'
$ curl -X POST 'http://127.0.0.1:8080/put?key=A3&value=Airplane3'
$ curl -X POST 'http://127.0.0.1:8080/put?key=A4&value=Airplane4'
```

```
Output: Omit
```

```bash
$ curl -X GET 'http://127.0.0.1:8080/queryall'
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
```bash
$ curl -X GET 'http://127.0.0.1:8080/query?key=K'
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
```bash
$ curl -X GET 'http://127.0.0.1:8080/query?key=A'
```
```
Output: 
        {
        "data": [
        "(A1, Airplane1)",
        "(A2, Airplane2)",
        "(A3, Airplane3)",
        "(A4, Airplane4)"
        ],
        "status": "OK"
        }
```
```bash
$ curl -X POST 'http://127.0.0.1:8080/shutdown'
```
```
Output: 
        Server shutting down...
```
```bash
$ curl -X POST 'http://127.0.0.1:8080/getProperty?name=leveldb.stats'
```
```
Output: 
        Compactions
        Level | Tables | Size(MB) | Time(sec) | Read(MB) | Write(MB)
        ------+--------+----------+-----------+----------+----------
        0 | 0 | 0.00000 | 1.5889 | 0.00000 | 9.32476
        1 | 75 | 100.20348 | 26.92093 | 231.49293 | 224.07294

        <property value or None return from DB::GetProperty()>
```
