import os


# noinspection SpellCheckingInspection
class TestData:
    google_debug_token = {
        "user": {
            "auth_token": os.getenv('GOOGLE_DEBUG_TOKEN'),
            "refresh_token": os.getenv('GOOGLE_DEBUG_REFRESH_TOKEN')
        }
    }

    post_article = {
        "article": {
            "title": "Yet another Sand Blog",
            "description": "Sand is m testing",
            "body": "another that am doin test"
        }
    }

    post_article_missing_data = {
        "article": {
            "title": "Yet another Sand Blog",
            "body": "another that am doin test"
        }
    }

    update_article = {
        "article": {
            "title": "Updating Yet another Sand Blog",
            "description": "Sand is m testing",
            "body": "another that am doing test"
        }
    }

    user_name = "iroq"
    user_email = "iroq@sims.andela"
    password = "teamiroq1"
