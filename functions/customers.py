from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.customers import Customers
from utils.pagination import pagination,check_model


def all_customers(status, search, page, limit, db):
    customers = db.query(Customers).options(joinedload(Customers.user)  )
    if search:
        search_formatted = "%{}%".format(search)
        customers = customers.filter(
            Customers.name.ilike(search_formatted) | Customers.comment.ilike(search_formatted) | Customers.number.ilike(
                search_formatted))

    if status in [True, False]:
        customers = customers.filter(Customers.status == status)
    customers = customers.order_by(Customers.id.desc())
    return pagination(customers, page, limit)


def create_customer(form, thisuser, db):
    new_customer_db = Customers(
        full_name=form.name,
        phone=form.phone,
        comment=form.comment,
        user_id=thisuser.id
    )
    db.add(new_customer_db)
    db.flush()
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_customer(db, ident):
    the_item = db.query(Customers).options(joinedload(Customers.user),
                                           ).filter(Customers.id == ident).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday customer mavjud emas")


def update_customer(form, thisuser, db):
    customer = check_model(db=db, model=Customers, id=form.id)
    db.query(Customers).filter(Customers.id == form.id).update({
        Customers.full_name: form.name,
        Customers.phone: form.number,
        Customers.comment: form.comment,
        Customers.user_id: thisuser.id
    })

    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")



