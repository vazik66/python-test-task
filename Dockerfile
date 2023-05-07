FROM python:3.11-slim

# Update image
RUN apt-get update && \
    apt-get upgrade -y


ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 


COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt


RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser


COPY /src ./src


CMD ["python", "-m", "src.main"]
