FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY ./app /app
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
