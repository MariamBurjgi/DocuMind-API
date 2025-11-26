FROM python:3.11-slim

# ვქმნით სამუშაო საქაღალდეს
WORKDIR /app

# ვაკოპირებთ ფაილებს
COPY . .

# ვაინსტალირებთ ბიბლიოთეკებს
RUN pip install --no-cache-dir -r requirements.txt

# ვუშვებთ სერვერს (Render იყენებს პორტს 10000)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]