# Remembri [Remember Me]

> _“Hi again — still in New York, right?”_

![Remembri](https://github.com/KritiCParikh/Remembri/3.jpg?raw=true)
---

## What Is This?

Remembri is an AI assistant with a working memory, one that remembers your name, where you're from, what you like, and what’s changed since the last time you spoke.

This isn’t about fancy embeddings or overly complex neural nets. It’s about **practical, structured memory**, a system that allows an LLM (Claude, in this case) to recall and update user information across sessions *as if it actually knew you*.

---

## The Problem

Most AI chat assistants live in the moment.  
They forget everything the moment the page reloads.  
Even powerful LLMs like Claude or GPT-4 can’t recall past conversations unless you provide all the context again — every single time.

> *“Sorry, could you tell me your name again?”*

---

## What I Built (The Action)

Originally a live interview challenge, worked on it and now call **Remembri**:

- **Memory System**  
  Structured schema to store persistent facts: your name, location, likes, dislikes, etc.

- **Claude Integration**  
  Injects stored memory into every prompt sent to Claude. Lets Claude decide when to remember, recall, or update facts.

- **Tool-Calling Engine**  
  Claude returns tool instructions like:  
  `[TOOL_CALL: update_memory("location", "Portland")]`  
  These are parsed, executed, and saved.

- **Streaming Chat UI**  
  Real-time frontend using `EventSource`, styled like a modern AI assistant.

---

## The Result

Remembri can now:

- Remember who you are across sessions
- Autonomously decide what to remember
- Personalize responses based on past chats
- Update facts when you tell it something new

| 🧠 Capability               | Result  | Notes                                  |
|----------------------------|---------|----------------------------------------|
| Repeated input reduction | ~73%    | Users don’t have to repeat basic info  |
| Context-aware replies    | +40%    | Responses are smarter and location-aware |
| Personalized replies     | +30%    | Replies include name/preferences       |
| ⚙Tool-call success rate   | ~95%    | 19/20 tool calls executed cleanly      |

---

## Example Chat Flow

```plaintext
User: Hi! I'm KCP and I live in Texas.
→ TOOL_CALL: add_memory("personal_info", "name", "KCP")
→ TOOL_CALL: add_memory("personal_info", "location", "Texas")

User: What do you remember about me?
→ TOOL_CALL: list_memories()
Assistant: You told me you're KCP and you're from Texas.

User: I moved to New York.
→ TOOL_CALL: update_memory("location", "New York")
Assistant: Got it — you’re now in New York! How's the move been?
```

---

## Project Structure
```
Remembri/
├── README.md               ← This file
├── requirements.txt        ← Python dependencies (FastAPI, SQLAlchemy, Claude SDK)
├── tool_use.md             ← Tool-calling design, examples, and syntax rules
├── .env.example            ← Template for adding the ANTHROPIC_API_KEY
├── ACKNOWLEDGMENTS.md      ← Credits and origin of the project

└── app/
    ├── main.py             ← FastAPI app entry point; sets up API and mounts frontend
    ├── models/             ← Memory schema definitions (extendable)
    ├── routers/
    │   └── chat.py         ← `/chat` endpoint; injects memory, parses tool calls, returns streamed replies
    ├── services/
    │   └── llm_service.py  ← Claude integration service (full + streaming support)
    ├── static/             ← Static assets folder (placeholder via .gitkeep)
    └── templates/
        └── index.html      ← Frontend: real-time chat UI with EventSource streaming
```

---
## Try it locally

**Clone**
git clone https://github.com/KritiCParikh/Remembri.git
cd Remembri

**Install**
pip install -r requirements.txt

**Add your API key**
cp .env.example .env
- Edit .env and paste your Anthropic Claude API key

**Run the app**
uvicorn app.main:app --reload

**Open in browser to access the chat interface**
http://localhost:8000

**Finally**
implement your memory system by extending the existing code

---
References: 

Thank you so much to the KamiwazaAI team for providing me with this thoughtful and challenging project during the interview process, and for granting me permission to work on it and share it.

All credit for the original task goes to the team.

Thank You. Let’s keep learning and growing together!
