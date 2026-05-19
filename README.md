# AI Chat Application

## Demo

https://github.com/user-attachments/assets/37a5b9e2-1593-480e-bf6c-6247ad2fd089



(https://youtu.be/-1Tm88O-D5o)


🚀 AI Chat Application with Streaming & Memory

A full-stack AI-powered chat application built using **FastAPI, Ollama (LLaMA3), Redis, and a modern web UI**.  
This project demonstrates a real-world AI chatbot with authentication, streaming responses, and multi-session chat management similar to ChatGPT.

---

## ✨ Features

- 🔐 JWT-based Authentication (Login / Signup)
- 💬 Multi-chat sessions (ChatGPT-style sidebar)
- ⚡ Real-time Streaming AI responses
- 🧠 Conversation memory using Redis
- 🗂️ Chat history with session management
- ✏️ Rename chat sessions
- 🗑️ Delete chat with confirmation
- 📋 Copy AI responses
- 🔄 Token expiry handling (auto logout)
- 📱 Responsive and modern UI

## Tech Stack

-   FastAPI
-   Ollama (LLaMA3)
-   Redis
-   HTML/CSS/JS

## Setup

1.  Run Redis
2.  Run Ollama
3.  Start backend: uvicorn main:app --reload
4.  Start frontend: python3 -m http.server 3000


## ⚙️ Installation & Setup

### 1. Clone Repository

git clone https://github.com/YOUR_USERNAME/ai-chat-app.git cd
ai-chat-app

### 2. Install Dependencies

pip install fastapi uvicorn redis python-jose

### 3. Start Redis

redis-server

### 4. Start Ollama

ollama serve ollama run llama3

### 5. Run Backend

uvicorn main:app --reload

### 6. Run Frontend

cd public python3 -m http.server 3000

Open: http://localhost:3000/login.html

------------------------------------------------------------------------

## 🔑 API Endpoints

### POST /signup

Register new user

### POST /login

Login and get JWT token

### POST /chat-stream

Stream AI response

### GET /history/{session_id}

Fetch chat history

------------------------------------------------------------------------

## 🧠 Architecture

The application follows a modular full-stack architecture with clear separation between frontend, backend, AI model, and memory layer.

┌──────────────────────┐
│      Frontend UI     │
│ (HTML, CSS, JS)      │
└─────────┬────────────┘
          │ HTTP (REST + Streaming)
          ▼
┌──────────────────────┐
│   FastAPI Backend    │
│ - Auth (JWT)         │
│ - Chat APIs          │
│ - Session Handling   │
└─────────┬────────────┘
          │
   ┌──────┴─────────┐
   ▼                ▼
┌──────────────┐  ┌────────────────┐
│   Ollama LLM │  │     Redis      │
│ (LLaMA3)     │  │ (Chat Memory)  │
└──────────────┘  └────────────────┘


## Flow Explanation
User sends a message from the frontend UI
Request goes to FastAPI backend with JWT authentication
Backend:
Retrieves chat history from Redis
Formats prompt with previous conversation
Request is sent to Ollama (LLM)
Ollama generates response (streaming)
Backend streams response back to frontend
Final response is stored in Redis for future context
## ⚡ Key Design Decisions
Streaming Response: Improves UX with real-time typing effect
Redis Memory: Enables session-based chat history
JWT Authentication: Secures user sessions
Modular Backend: Easy to replace LLM (Ollama → OpenAI, etc.)
## 🔧 Scalability Considerations
Redis can be replaced with distributed cache (AWS ElastiCache)
Backend can be scaled using load balancers
LLM can be swapped with cloud APIs (OpenAI, Claude)
Session handling supports multi-user environments

## Author

## Rahul Mehndiratta
Senior Mobile Developer → AI Engineer 🚀
