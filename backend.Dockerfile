FROM python:3.10

WORKDIR /backend

ENV TZ=Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY backend /backend

ENV PYTHONPATH=/backend

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "application.py"]
