#! /usr/bin/python
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markupsafe import Markup
from model import load_model, labelling, occurrences, principal
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

@app.get("/")
def hello_user(request: Request):
    return templates.TemplateResponse('accueil.html', context={'request': request})

@app.post("/")
def form_post(request: Request, message: str = Form(...)):
    model = load_model()
    results = labelling(message, model)
    occurrence = occurrences(results)
    princ = principal(results)
    response = Markup(results)
    return templates.TemplateResponse('resultats.html', context={'request': request,'response': response,'occurrence':occurrence, 'princ':princ})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)