# MLAPI-fastAPI

## Features

### Routes

```bash
Endpoint              Methods  Rule
-----------------     -------  -----------------------
routers.image          GET      /images
routers.image          POST     /images
routers.probabilities  POST     /probabilities/{file_id}
```

### User Story

- User can show pictures' names and file_id.
- User can upload picture files.
- User can see result of number predict.

## Usage

### Make learned MLapi

Execute below code in analysis.ipynb

```bash
import pickle
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

digits = load_digits()
X = digits.data
y = digits.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)

logreg = LogisticRegression(max_iter=2000)
model = logreg.fit(X_train, y_train)
with open('model.pickle', mode='wb') as fp:
    pickle.dump(model, fp)
```

### Build docker image

```bash
$ docker-compose build
```

### Setting python environment by poetry

```bash
$ docker-compose run \
  --entrypoint "poetry init \
    --name ml-api \
    --dependency fastapi \
    --dependency uvicorn[standard]" \
  ml-api
```

### Install fastAPI

```bash
$ docker-compose run --entrypoint "poetry install" ml-api
```

### Start API

```bash
$ docker-compose up
```

### Migrate DB

```bash
docker-compose exec ml-api poetry run python -m api.migrate_db

CREATE TABLE image_info (
        id INTEGER NOT NULL AUTO_INCREMENT, 
        file_id VARCHAR(255), 
        filename VARCHAR(1024), 
        PRIMARY KEY (id)
)
```

### Check DB table

```bash
$ docker-compose exec db mysql demo

mysql> SHOW TABLES;
+----------------+
| Tables_in_demo |
+----------------+
| image_info     |
+----------------+
1 row in set (0.11 sec)

mysql> DESCRIBE image_info;
+----------+---------------+------+-----+---------+----------------+
| Field    | Type          | Null | Key | Default | Extra          |
+----------+---------------+------+-----+---------+----------------+
| id       | int           | NO   | PRI | NULL    | auto_increment |
| file_id  | varchar(255)  | YES  |     | NULL    |                |
| filename | varchar(1024) | YES  |     | NULL    |                |
+----------+---------------+------+-----+---------+----------------+
3 rows in set (0.20 sec)
```

## Testing

### Execute test command

```bash
docker-compose run --entrypoint "poetry run pytest --asyncio-mode=auto" ml-api 
```

FYI:
https://github.com/pytest-dev/pytest-asyncio
