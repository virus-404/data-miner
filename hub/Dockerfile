FROM python:3
WORKDIR /usr/src/dataminer
COPY requirements.txt ./
RUN pip3 install --upgrade pip 
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /usr/src/dataminer
CMD [ "python3", "main.py" ]

#For ANY change user docker-compose build _container_  ==> docker-compose up _container_