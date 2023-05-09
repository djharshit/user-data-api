FROM python

ENV HOST="mongodb://127.0.0.1:27017/"

WORKDIR /home/user

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python app.py --host $HOST
