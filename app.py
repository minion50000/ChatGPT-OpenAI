from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Replace 'your_openai_api_key' with your actual OpenAI API key
api_key = os.environ.get('OPENAI_API_KEY')

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_response")
async def get_response(request: Request):
    data = await request.json()
    user_input = data.get('message')
    model_type = data.get('model', 'gpt-4')  # Default to gpt-4 if not provided
    
    chat_gpt = ChatOpenAI(api_key=api_key, model=model_type, temperature=0)
    
    messages = [
        HumanMessage(content=user_input),
    ]
    ai_message = chat_gpt.invoke(messages)
    return JSONResponse(content={'response': ai_message.content})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5555)
