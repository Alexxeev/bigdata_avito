from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
import pandas as pd
import numpy as np
import pickle

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

def build_regress_model(df: pd.DataFrame, y: pd.Series) -> RandomForestRegressor:
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.33)
    rfr = RandomForestRegressor(n_estimators=100, n_jobs=2)
    rfr.fit(X_train, y_train)
    predicted_reg = rfr.predict(X_test)
    print(f"Mean error = {mean_absolute_percentage_error(y_test, predicted_reg) * 100:.3f} %")
    return rfr

def dump_regress_model(rfr: RandomForestRegressor):
    pickle.dump(rfr, open("flatz.pkl", "wb"))


def predict(request: list, model):
    prediction = model.predict(np.array(request))
    output = [prediction[0]]
    return output