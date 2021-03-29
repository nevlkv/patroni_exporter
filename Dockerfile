FROM python:alpine
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
WORKDIR /
COPY requirements.txt patroni_exporter.py  /
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "/patroni_exporter.py" ]
