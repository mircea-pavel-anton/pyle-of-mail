# The output of python3 --version from the dev machine: Python 3.8.5
FROM python:3.8-slim-buster

# Create the dir that will hold the source files
RUN mkdir /src

# Set the newly created dir as the workdir
WORKDIR /src

# Copy over the essential files:
#  - main.py & functions.py to be able to run our code
#  - requirements.txt to be able to prepare the environment
# We do not need the config.py file, as that will be bind
# mounted
COPY src/main.py .
COPY src/functions.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD python3 -u /src/main.py
