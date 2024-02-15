import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.trades import one_trade
from models.products import Products
from utils.pagination import pagination


def all_products(status, search, start_date, end_date,  page, limit, db):
    products = db.query(Products).options(joinedload(Products.user),
                                          joinedload(Products.trade),
                                          )
    if search:
        search_formatted = "%{}%".format(search)
        products = products.filter(
            Products.price.ilike(search_formatted) | Products.trade_price.ilike(search_formatted))

    if status in [True, False]:
        products = products.filter(Products.status == status)



    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
        products = products.filter(Products.created_at >= start_date, Products.created_at <= end_date)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
    products = products.order_by(Products.id.desc())
    return pagination(products, page, limit)


def create_payment(form, thisuser, db):
    trade = one_trade(db=db, id=form.trade_id)
    if trade.status:
        raise HTTPException(status_code=200, detail=f"Ushbu savdo tugatilgan")
    new_payment_db = Products(
        amount=form.money,
        trade_id=form.trade_id,
        user_id=thisuser.id,
        created_at=datetime.datetime.now()
    )
    db.add(new_payment_db)
    db.flush()
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_payment(db, ident):
    the_item = db.query(Products).options(joinedload(Products.user),
                                          joinedload(Products.trade),
                                          ).filter(Products.id == ident).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday payment mavjud emas")



