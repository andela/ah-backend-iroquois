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

    post_article_with_tags = {
        "article": {
            "title": " The last week of sems1",
            "description": "Sims1 is ending this week and it has been intersting",
            "body": "I had enough time to make this short.",
            "tags": ["Django", "Python", "Java", "SpringBoot", "Hibernate", "PrimeFaces"]
        }
    }

    post_tag = {
        "tag_name": "Django"
    }

    update_tag = {
        "tag_name": "django_restful"
    }

    update_tag_on_article_data = {
        "article": {
            "title": "The last week of sems1",
            "description": "Sims1 is ending this week and it has been intersting",
            "body": "I had enough time to make this short.",
            "tags": ["Django Restful"]
        }
    }

    user_name = "iroq"
    user_email = "iroq@sims.andela"
    password = "teamiroq1"

    post_article_tags = {
        "article": {
            "title": "Yet another Sand Blog",
            "description": "Sand is m testing",
            "body": "another that am doin test",
            "tags": ["python", "software", "english"]
        }
    }
