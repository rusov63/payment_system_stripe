FROM python:3.12-slim
## Debian GNU/Linux 10, python без компилятора

## устанавливаем рабочую директорию внутри контейнера.
WORKDIR /projects_payments

## Копируем и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

## Копируем все файлы из текущей директории в рабочую директорию контейнера
COPY . .

## Команда запуска контейнера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "projects_payments.wsgi:application"]