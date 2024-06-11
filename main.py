import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from logic import get_articles

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


@app.post("/generate", response_class=HTMLResponse)
async def compute(request: Request, language: str = Form(), level: str = Form()):
    articles = await get_articles(language=language, level=level)
    context = {
        "request": request,
        "articles": articles,
    }
    return templates.TemplateResponse("result.html", context)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
