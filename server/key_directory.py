from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

key_store = {}

class UserKey(BaseModel):
    username:str
    public_key:str

@app.post("/register")
def register_key(user: UserKey):
    key_store[user.username] = user.public_key
    return {"status": "success", "message":  f"Key for {user.username} saved"}

@app.get("/keys/{username}")
def get_key(username: str):
    if username not in key_store:
        raise HTTPException(status_code=404, detail="User not found")

    return {"username": username, "public_key": key_store[username]}
