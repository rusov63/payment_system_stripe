FROM python:3.10-slim
## Debian GNU/Linux 10, python без компилятора

## устанавливаем рабочую директорию внутри контейнера.
WORKDIR /payment_system_stripe

## Копируем и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

## Копируем все файлы из текущей директории в рабочую директорию контейнера
COPY . .

ENV PYTHONPATH=/payment_system_stripe

# Выполняем команду collectstatic
RUN python manage.py collectstatic --noinput

## Команда запуска контейнера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
