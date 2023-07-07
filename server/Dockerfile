    FROM python:3.8.2
    ENV PYTHONBUFFERED 1
    ENV PYTHONWRITEBYTECODE 1
    RUN apt-get update \
        && apt-get install -y netcat
    ENV APP=/djangoapp
    # Change the workdir.
    WORKDIR $APP
    # Install the requirements
    COPY requirements.txt $APP
    RUN pip3 install -r requirements.txt
    # Copy the rest of the files
    COPY . $APP
    EXPOSE 8000
    COPY /djangoapp/entrypoint.sh .
    RUN chmod +x /djangoapp/entrypoint.sh
    ENTRYPOINT ["/bin/bash","/djangoapp/entrypoint.sh"]
    CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]