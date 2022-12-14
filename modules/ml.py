from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import pickle

columns = pd.Index(['area', 'livingArea', 'rooms', 'floor', 'total_floor', 'buildYear',
       'time_from_metro_min'])
scaler = pickle.load(open('model/scaler.pkl', 'rb'))

def build_model(filename: str):
    df = read_csv(filename)
    df[0] = preprocess_data(df[0])
    df[1] = scale_price(df[1])
    rfr = build_regress_model(df[0], df[1])
    dump_regress_model(rfr)

def read_csv(filename: str) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(filename, sep=";", skipinitialspace=True, usecols=np.arange(18))
    df.pop("offer_id")
    df.pop("date")
    df.pop("geo_point")
    df.pop("address")
    df.pop("passengerLiftsCountl")
    y = df.pop("price")
    return df, y

def preprocess_data(df: pd.DataFrame):
    df.replace("None", np.nan, inplace=True)
    df.livingArea = pd.to_numeric(df.livingArea)
    df.rooms = pd.to_numeric(df.rooms)
    df.buildYear = pd.to_numeric(df.buildYear)
    print(df.dtypes)
    numeric_variables = list(df.dtypes[df.dtypes != "object"].index)
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer = imputer.fit(df[numeric_variables])
    df[numeric_variables] = imputer.transform(df[numeric_variables])
    df.rooms = df.rooms.apply(np.int64)
    df.buildYear = df.buildYear.apply(np.int64)

def scale_price(y: pd.Series):
    #scaler = MinMaxScaler((1, 10))
    y_norm = scaler.fit_transform(np.reshape(y.values, (-1, 1)))
    return y_norm.ravel()

def build_regress_model(df: pd.DataFrame, y: pd.Series) -> RandomForestRegressor:
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.33)
    rfr = RandomForestRegressor(n_estimators=100, n_jobs=2)
    rfr.fit(X_train, y_train)
    predicted_reg = rfr.predict(X_test)
    print(f"Mean error = {mean_absolute_percentage_error(y_test, predicted_reg) * 100:.3f} %")
    return rfr

def dump_regress_model(rfr: RandomForestRegressor):
    pickle.dump(rfr, open("model/flatz.pkl", "wb"))


def predict(request: list, model: RandomForestRegressor):
    df = pd.DataFrame([request])
    df.columns = columns
    prediction = model.predict(df)
    prediction_unscaled = scaler.inverse_transform(np.reshape(prediction, (-1, 1)))
    prediction_flattened = prediction_unscaled.ravel()
    return round(prediction_flattened[0])