# MLAPI-fastAPI

## Features

### Routes

```bash
Endpoint           Methods  Rule
-----------------  -------  -----------------------
api.health         GET      /v1/health
api.file_upload    POST     /v1/file-upload
api.probabilities  POST     /v1/probabilities
```

### User Story

- User can check health status.
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
