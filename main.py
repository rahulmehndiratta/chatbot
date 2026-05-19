from fastapi import FastAPI, Header, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import requests
import redis
import json

from auth import hash_password, verify_password, create_token, decode_token

# ---------- Redis ----------
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

app = FastAPI()
users_db = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- AUTH ----------

class SignupRequest(BaseModel):
    username: str
    password: str

@app.post("/signup")
def signup(req: SignupRequest):
    if req.username in users_db:
        return {"error": "User already exists"}

    users_db[req.username] = {
        "password": hash_password(req.password)
    }

    return {"message": "User created"}


class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(req: LoginRequest):
    user = users_db.get(req.username)

    if not user or not verify_password(req.password, user["password"]):
        return {"error": "Invalid credentials"}

    token = create_token({"sub": req.username})
    return {"token": token}


# ---------- AUTH HELPER ----------

def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Token expired")


# ---------- MODELS ----------

class Request(BaseModel):
    question: str
    session_id: str


# ---------- REDIS ----------

def get_chat(key):
    try:
        data = redis_client.get(key)
        return json.loads(data) if data else []
    except:
        return []

def save_chat(key, history):
    redis_client.setex(key, 3600, json.dumps(history))


# ---------- PROMPT ----------

def format_messages(messages):
    prompt = "You are a helpful assistant. Answer briefly and clearly.\n\n"

    for msg in messages:
        if msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
        else:
            prompt += f"Assistant: {msg['content']}\n"

    prompt += "Assistant:"
    return prompt


# ---------- STREAMING API (SECURED) ----------

@app.post("/chat-stream")
def chat_stream(req: Request, user=Depends(get_current_user)):
    key = f"user:{user}:chat:{req.session_id}"

    history = get_chat(key)
    history.append({"role": "user", "content": req.question})

    def generate(history_ref):
        full_response = ""

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": format_messages(history_ref),
                    "stream": True
                },
                stream=True,
                timeout=60
            )

            for line in response.iter_lines():
                if not line:
                    continue

                try:
                    data = json.loads(line.decode("utf-8"))
                    chunk = data.get("response")

                    if chunk:
                        full_response += chunk
                        yield chunk
                except:
                    continue

        except Exception:
            yield "Error: AI failed"

        # save response
        history_ref.append({"role": "assistant", "content": full_response})
        history_ref[:] = history_ref[-10:]
        save_chat(key, history_ref)

    return StreamingResponse(generate(history), media_type="text/plain")


# ---------- NORMAL API (SECURED) ----------

@app.post("/ask")
def chat(req: Request, user=Depends(get_current_user)):
    key = f"user:{user}:chat:{req.session_id}"

    history = get_chat(key)
    history.append({"role": "user", "content": req.question})

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": format_messages(history),
            "stream": False
        }
    )

    answer = response.json().get("response", "No response")

    history.append({"role": "assistant", "content": answer})
    history = history[-10:]
    save_chat(key, history)

    return {"answer": answer}


# ---------- HISTORY (SECURED) ----------

@app.get("/history/{session_id}")
def get_history(session_id: str, user=Depends(get_current_user)):
    key = f"user:{user}:chat:{session_id}"
    return {"history": get_chat(key)}


# ---------- BASIC ----------

@app.get("/")
def home():
    return {"message": "Hello Rahul 🚀"}