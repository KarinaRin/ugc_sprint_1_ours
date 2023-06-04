def pipeline_list_reviews(field_name, field_value):
    query = {"$and": [
        {"review": {"$ne": {}, "$type": "object"}},
        {field_name: field_value}
    ]}
    return query


def pipeline_exist_review(film_id, user_id):
    """...если пользователь ПИСАЛ рецензию к фильму
    """
    return {
        "film_id": film_id,
        "email": user_id
    }


# TODO: надо починить
def pipeline_count_review(film_id, author_id, field_name, user_id):
    return {
        "film_id": film_id,
        "email": author_id
    }
