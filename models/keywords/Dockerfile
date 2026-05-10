FROM python:3.12-slim

WORKDIR /

COPY models/keywords/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY common/ ./common/
COPY models/keywords ./common/keywords/

EXPOSE 8000

CMD ["uvicorn", "models.keywords.main:app", "--host", "0.0.0.0", "--port", "8000"]