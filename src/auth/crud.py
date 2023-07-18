from sqlalchemy.orm import Session
from . import models, schemas
from .utils import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: models.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_esg_report(db: Session, report_id: int):
    return db.query(models.EsgReport).filter(models.EsgReport.id == report_id).first()


def create_esg_report(db: Session, user: models.User, esg_report: str):
    report = models.EsgReport(user_id=user.id, esg_report=esg_report)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def update_esg_report(db: Session, report: models.EsgReport):
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def delete_esg_report(db: Session, report_id: int):
    report = db.query(models.EsgReport).filter(models.EsgReport.id == report_id).first()
    db.delete(report)
    db.commit()
