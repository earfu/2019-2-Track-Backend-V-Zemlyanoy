FROM python:3.8
ADD . /messanger
RUN pip install -r messanger/requirements.txt
EXPOSE 8000
