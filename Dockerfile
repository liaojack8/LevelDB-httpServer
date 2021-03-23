FROM python:3.9

WORKDIR /home/LevelDB-httpServer

COPY . .

RUN pip install cython numba plyvel flask

ENTRYPOINT ["python", "server.py"]
