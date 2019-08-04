
FROM python:3

RUN apt -y -q update \
 && apt -y -q upgrade \
 && apt -y -q install ncat

WORKDIR /usr/src/app

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install .

#CMD [ "python", "./geminidata-service.py" ]
CMD [ "geminidata-service.py" ]

