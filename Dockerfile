FROM python:3.9

# define the pwd ( present working directory)
WORKDIR /chatbot

ADD . /chatbot

# installing the dependecies
RUN pip install -r requirements.txt

# command to satrt the container
CMD ["python", "chatbot.py"]