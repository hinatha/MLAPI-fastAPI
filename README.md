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

- User can show pictures' names.
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
