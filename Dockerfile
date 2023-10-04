FROM python:3.11.5-bookworm

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
