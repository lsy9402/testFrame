from fastapi import FastAPI, Body

app = FastAPI()


@app.post("/test")
def test(body=Body(...)):
    return body


if __name__ == '__main__':
    from uvicorn import run

    run("main:app")
