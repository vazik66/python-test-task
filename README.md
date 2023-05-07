# Aiohttp test task

## Task
Create REST API:
- GET /convert?fromRUR&to=USD&amount=42
Convert amount from currency 'from' to currency 'to'

- POST /database?merge=1
Set data to currency
If merge == 0, old data is invalidated
If merge == 1, New data updates old, but if not updated old data stays actual 

- Responses are in json

## How to use
### 1. Fill in .env file
```shell
cat .env.example >> .env
```
### 2. Start server
#### Docker
```shell
docker compose up -d
```

#### Console
1. Start redis and change REDIS_HOST, REDIS_PORT, REDIS_PASSWORD in .env file
2. Create virtual environment
```shell
python -m venv venv
````

3. Activate virtual environment
```shell
source venv/bin/activate 
```

4. Download dependencies
```shell
pip install -r requirements.txt
```
5. Run from root folder
```shell
python -m src.main
```

### cURL
- Convert currency:
	- query: from, to, amount
```shell
curl localhost:8080/convert?from=USD&to=RUR&amount=42
>>> {"result": 1260}
```

- Update data:
	- query: `?merge=1` (1/0)
	- body: `{"pairs": [{"currency_pair": "USD/RUR", "rate": 76.2}]}`
```shell
curl -d '{"pairs": [{"currency_pair": "USD/RUR", "rate": 76.2}, {"currency_pair": "USD/EUR", "rate": 0.87}]}' "localhost:8080/database?merge=1"
```

### Test
```shell 
pip install -r requirements.dev.txt
python -m pytest --asyncio-mode=auto
```
