FROM python:3.10.5

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

# ENV HOST https://localhost

# ENV PORT 8000

# EXPOSE ${PORT}

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]