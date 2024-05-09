FROM python:3.12

WORKDIR /app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/api  

EXPOSE 8000

COPY entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint to the custom script
ENTRYPOINT ["entrypoint.sh"]


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
