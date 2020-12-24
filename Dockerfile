FROM python:3.6
WORKDIR /main
COPY . /main
RUN pip install -r /main/requirements.txt
CMD ["python", "mail_app.py"]