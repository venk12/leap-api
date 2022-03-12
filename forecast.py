import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from neuralprophet import NeuralProphet
import json

def convertDate(n):
    return (datetime.utcfromtimestamp(0) + timedelta(n)).strftime("%Y-%m-%d")

def forecast(df, dateField, valueField):
    # df['date'] = df['date'].strftime("%Y-%m-%d")
    print(df.head())
    df['new_date'] = df['date'].apply(convertDate)     
    df['new_date'] = pd.DatetimeIndex(df['new_date'])
    
    df['new_datetime'] = pd.to_datetime(df['new_date'])  
    df = df.sort_values(by='new_datetime')
    
    df['value'] = df['value'].astype(int)

    df['first_day'] = df['new_date'] - df['new_date'].dt.weekday * np.timedelta64(1, 'D')

    df = df.rename(columns={'first_day': 'ds', 'value': 'y'})
    df = df.groupby(['ds']).sum().reset_index()    
    df.drop(df.columns.difference(['ds','y']), 1, inplace=True)

    m = NeuralProphet()
    metrics = m.fit(df, freq="W")
    future = m.make_future_dataframe(df, periods=15)
    forecast = m.predict(future)
    forecast = forecast[['ds', 'y', 'yhat1']]
    forecast = forecast.rename(columns={'yhat1': 'pred'})

    df["pred"] = ""
    df_forecast_res = df.append(forecast)
    df_forecast_res = df_forecast_res.rename(columns={'ds': 'date', 'y':'actual'})
    result = df_forecast_res.to_json(orient="split")
    parsed = json.loads(result)

    return parsed