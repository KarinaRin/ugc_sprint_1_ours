from datetime import datetime


def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_email_film_id(email, film_id):
    return email + str(film_id) + ','
