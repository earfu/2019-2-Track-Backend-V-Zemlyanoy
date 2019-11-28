FROM python:3.7
ADD . /messanger
RUN pip install -r /messanger/requirements.txt
EXPOSE 8000
WORKDIR /messanger