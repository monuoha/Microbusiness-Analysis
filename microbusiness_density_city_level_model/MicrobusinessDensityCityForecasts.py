from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
#from prophet.serialize import model_to_json
import pickle
import numpy as np
from prophet import Prophet
from fastapi.responses import RedirectResponse

app = FastAPI(title = 'Microbusiness Density City-Level Forecasting Service')

with open('microbusiness_density_city_level_model.pkl', 'rb') as f:
    model = pickle.load(f)
    
#Request body structure
class ForecastRequest(BaseModel):
    months_to_predict: int

@app.get('/')
def redirect_to_docs():
    return RedirectResponse(url="/docs") 

@app.post('/predict')
def predict(request: ForecastRequest):
    try:

        x1 = np.load('engagement_index_city.npy')

        dates = pd.read_csv('dates.csv')

        regressor = pd.DataFrame({'ds': np.array(dates).flatten(), 'y': x1})

        regressor_proph = Prophet(daily_seasonality = True, weekly_seasonality = True, yearly_seasonality = True, seasonality_mode = 'multiplicative')
        regressor_model = regressor_proph.fit(regressor)

        regressor_future = regressor_model.make_future_dataframe(periods = request.months_to_predict, freq = 'MS')
        regressor_forecast = regressor_model.predict(regressor_future)
        regressor_forecast.rename(columns = {'yhat': 'x1'}, inplace = True)



        #Generate future dataframe
        future = model.make_future_dataframe(periods = request.months_to_predict, freq = 'MS')

        x1 = pd.merge(regressor_forecast, future, on = 'ds', how = 'inner')
        x1 = x1['x1']

        future['x1'] = x1

        #Generate future calculations
        forecast = model.predict(future)

        #Timestamps and Predictions
        output = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(request.months_to_predict)
        output['ds'] = output['ds'].dt.strftime('%Y-%m-%d')

        return output.to_dict(orient = 'records')
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))