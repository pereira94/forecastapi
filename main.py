from fastapi import FastAPI, HTTPException
from model import convert, predict, train

app = FastAPI()


@app.get("/")
async def pong():
    return {"It works"}


@app.post("/predict", status_code=200)
def get_prediction(store = 1):

    prediction_list = predict(store)

    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {"store": store, "forecast": convert(prediction_list)}
    return response_object

@app.post("/train", status_code=200)
def train_model(storein = 7):
    train(data = '/Users/pedropereira/Desktop/train.csv', store = int(storein))
    return("Model trained")


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
