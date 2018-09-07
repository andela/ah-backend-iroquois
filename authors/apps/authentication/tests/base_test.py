"""
This module contains data used by other test modules
"""

class BaseTest():
    """
    This class contains data required for testing by test classes.
    """
    def __init__(self):
        self.user_name = "iroq"
        self.user_email = "iroq@sims.andela"
        self.password = "teamiroq1"
        self.superuser_name = "iroquois"
        self.superuser_email = "iroq@sims1.andela"
        self.superuserpassword = "teamiroq"
        self.user_data = {"user": {"username": self.user_name, "email": self.user_email,
                                   "password": self.password,
                                   }
                          }
        self.login_data = {"user": {"email": self.user_email, "password": self.password,
                                    }
                           }
        self.invalid_login_data = {"user": {"email": '',
                                            "password": self.password,
                                            }
                                   }
        self.invalid_reg_data = {"user": {"username": '', "email": '',
                                          "password": self.password,
                                          }
                                 }

        self.no_password_login = {
            "user": {"email": self.user_email,
                     "password": None,
                     }
        }
                                 