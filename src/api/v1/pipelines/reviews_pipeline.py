def pipeline_exist_doc(film_id, user_email):
    return {'film_id': film_id, 'email': user_email}


def pipeline_list_reviews(field_name, field_value):
    query = {"$and": [
        {"review": {"$ne": {}, "$type": "object"}},
        {field_name: field_value}
    ]}
    return query


def pipeline_exist_review(film_id, user_id):
    """...если пользователь ПИСАЛ рецензию к фильму
    """
    query = {"$and": [
        {"review": {"$ne": {}, "$type": "object"}},
        {'film_id': film_id},
        {'email': user_id}
    ]}
    return query


def pipeline_count_review(film_id, author_id, field_name, user_id):
    field_name = 'review.' + field_name
    query = {"$and": [
        {"review": {"$ne": {}, "$type": "object"}},
        {'film_id': film_id},
        {'email': author_id},
        {field_name: {'$in': [user_id]}}
    ]}
    return query
