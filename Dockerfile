FROM python:3.9.2-alpine

ENV APP_HOME /app
RUN mkdir ${APP_HOME}
WORKDIR ${APP_HOME}

COPY ./app ${APP_HOME}
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "heim:app"]
EXPOSE 8080
