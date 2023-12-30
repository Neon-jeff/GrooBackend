# Base image
FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create the appropriate directories
WORKDIR /stems

# install ubuntu packages required for
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    pkg-config \
    libcairo2-dev


# copy requirements into work directorty
COPY requirements.txt .
# install dependecies
RUN pip install -r requirements.txt



# copy project files and directories
COPY . .


# Port where the Django app runs
EXPOSE 8000

# Populate database and start server
CMD python3 manage.py migrate; gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
