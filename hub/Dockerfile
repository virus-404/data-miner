FROM python:3
WORKDIR /usr/src/dataminer
COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/dataminer
CMD [ "python", "main.py" ]

#For ANY change user docker-compose build _container_  ==> docker-compose up _container_