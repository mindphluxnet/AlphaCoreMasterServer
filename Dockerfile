# Use an official Python runtime as a parent image
FROM python:3.10-alpine
WORKDIR /app
COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8000
CMD ["python", "main.py"]

