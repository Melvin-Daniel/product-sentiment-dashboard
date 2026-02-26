from services.db_service import get_reviews_from_db

def get_all_reviews():
    return get_reviews_from_db()