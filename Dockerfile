# Образ python
FROM python:3.9

# Рабочая директория
WORKDIR /app

# Копирование файла python в рабочую директорию
COPY calc.py ./

# Копирование файла с зависимостями
COPY requirements.txt ./

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Порт
EXPOSE 5000

# Запуск калькулятора
CMD ["python","calc.py"]

