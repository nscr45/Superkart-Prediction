FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y     build-essential     curl     git     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip &&     pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 7860

HEALTHCHECK CMD curl --fail http://localhost:7860/health || exit 1

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:app"]
