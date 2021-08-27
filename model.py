import datetime
from pathlib import Path
import joblib
import pandas as pd
from fbprophet import Prophet

BASE_DIR = Path(__file__).resolve(strict=True).parent


def train(data, store):
    data = pd.read_csv(data)
    data = data[data['Store'] == store]
    df_forecast = data[['Date','Weekly_Sales']] 
    df_forecast.rename(columns={'Weekly_Sales':'y', 'Date':'ds'}, inplace=True)
    df_forecast

    model = Prophet()
    model.fit(df_forecast)

    joblib.dump(model, Path(BASE_DIR).joinpath(f"{store}.joblib"))

    return((min(df_forecast['ds']), max(df_forecast['ds'])))


def predict(store):
    start, last = train(data = '/Users/pedropereira/Desktop/train.csv', store = 1)
    model_file = Path(BASE_DIR).joinpath(f"{store}.joblib")
    if not model_file.exists():
        return False

    model = joblib.load(model_file)

    future = pd.to_datetime(last) + datetime.timedelta(days=14)

    dates = pd.date_range(start=pd.to_datetime(start), end=future)
    df = pd.DataFrame({"ds": dates})

    forecast = model.predict(df)

    return forecast.tail(14).to_dict("records")

def convert(prediction_list):
    output = {}
    for data in prediction_list:
        date = data["ds"].strftime("%m/%d/%Y")
        output[date] = data["trend"]
    return output

