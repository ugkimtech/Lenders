#use official python image
FROM python:3.11-slim

# set working directory
WORKDIR ./

# build arguments
ARG SECRET_KEY
ARG DATABASE_URL
ENV SECRET_KEY=$SECRET_KEY
ENV DATABASE_URL=$DATABASE_URL

# copy django project files
COPY . .
RUN ls
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput
# expose port for django
EXPOSE 8000

# start gunicon server
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn Lenders.wsgi:application --bind 0.0.0.0:8000