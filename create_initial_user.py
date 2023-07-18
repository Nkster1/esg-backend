from src.auth.crud import get_user_by_email, create_esg_report
from src.auth.database import SessionLocal

if __name__ == '__main__':
    db = SessionLocal()
    try:
        pass
        # uncomment if user does not exist
        # user = UserCreate(email="a@b.com", password="I like trains")
        # create_user(db, user)
    except Exception as e:
        print(e)
        # fine if user already created


    user_mail = "a@b.com"
    basic_report = " hi "

    user = get_user_by_email(db, user_mail)
    create_esg_report(db, user=user, esg_report=basic_report)
