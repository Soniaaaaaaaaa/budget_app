FROM  python:3.12-slim

RUN apt-get update \ 
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential default-libmysqlclient-dev pkg-config \ 
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --ignore-installed -r requirements.txt

COPY . .

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]
CMD ["main.py"]
