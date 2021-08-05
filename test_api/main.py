from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger

app = FastAPI()

user_table = [
    {
        "username": "test",
        "password": "test",
        "token": "test_token",
        "email": "test@email.com"
    }
]


@app.post("/login")
def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    for user in user_table:
        if form_data.username == user.get("username") and form_data.password == user.get("password"):
            return {"access_token": user.get("token"), "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="用户名或密码错误")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@app.post("/get_email")
def test(body: dict = Body(...), token: str = Depends(oauth2_scheme)):
    for user in user_table:
        if token == user.get("token"):
            body["username"] = user.get("username")
            body["email"] = user.get("email")
            break
    return body


if __name__ == '__main__':
    # from uvicorn import run
    #
    # run("main:app")
    print(logger.level("SUCCESS"))
    logger.info("SUCCESS")
