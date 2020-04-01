FROM python:3.8
ADD ./messanger /messanger
RUN pip install -r messanger/requirements.txt
EXPOSE 8000
