from passlib.context import CryptContext

from models.users import Users

pwd_context = CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException

from routes.auth import get_password_hash
from utils.pagination import pagination


def all_users(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Users.name.like(search_formatted) | Users.phone.like(search_formatted) | Users.username.like(
            search_formatted)
    else:
        search_filter = Users.id > 0
    if status in [True, False]:
        status_filter = Users.status == status
    else:
        status_filter = Users.id > 0

    if roll:
        roll_filter = Users.roll == roll
    else:
        roll_filter = Users.id > 0

    users = db.query(Users).filter(
        search_filter, status_filter, roll_filter).order_by(Users.id.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_user(id, db):
    return db.query(Users).filter(Users.id == id).first()


def user_current(user, db):
    return db.query(Users).filter(Users.id == user.id).first()


def create_user(form, user, db):
    user_verification = db.query(Users).filter(Users.username == form.username).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
    number_verification = db.query(Users).filter(Users.number == form.number).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

    new_user_db = Users(
        name=form.name,
        roll=form.roll,
        username=form.username,
        phone=form.phone,
        password=get_password_hash(form.password),

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_user(form, user, db):
    if one_user(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Users).filter(Users.username == form.username).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    db.query(Users).filter(Users.id == form.id).update({
        Users.name: form.name,
        Users.roll: form.roll,
        Users.username: form.username,
        Users.phone: form.phone,
        Users.status: form.status,

    })
    db.commit()

    return one_user(form.id, db)


def user_delete(id, db):
    if one_user(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Users).filter(Users.id == id).update({
        Users.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
