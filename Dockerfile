FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/db_of_templates

COPY ./req.txt /usr/src/req.txt
RUN pip install -r /usr/src/req.txt

COPY . /usr/src/db_of_templates

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
