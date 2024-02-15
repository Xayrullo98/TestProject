import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.sold_products import Sold_Products
from models.trades import Trades
from utils.pagination import check_model
from utils.pagination import pagination


def all_trades(status, search, page, limit, db):
    trades = db.query(Trades).options(
        joinedload(Trades.user),
    )
    if search:
        search_formatted = "%{}%".format(search)
        trades = trades.filter(
            Trades.price.ilike(search_formatted) | Trades.comment.ilike(search_formatted))

    if status in [True, False]:
        trades = trades.filter(Trades.status == status)
    trades = trades.order_by(Trades.id.desc())
    return pagination(trades, page, limit)


def create_trade(form, thisuser, db):
    number = last_trade(db, thisuser)
    if number.trade_number:
        new_number = int(number.trade_number) + 1
    else:
        new_number = 1
    products = form.products

    new_trade_db = Trades(
        amount=form.amount,
        customer_id=form.customer_id,
        trade_number=new_number,
        date=datetime.datetime.now(),
        user_id=thisuser.id
    )
    db.add(new_trade_db)
    db.flush()
    db.commit()
    for product in products:
        new_sold_products = Sold_Products(
            customer_id=form.customer_id,
            trade_id=new_trade_db.id,
            product_id=product.product_id,
            user_id=thisuser.id,
            number=product.number,
            created_at=datetime.datetime.now()

        )
        db.add(new_sold_products)
        db.flush()
        db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_trade(db, id):
    the_item = db.query(Trades).options(joinedload(Trades.user), joinedload(Trades.customer),
                                        ).filter(Trades.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday trade mavjud emas")


def last_trade(db, thisuser):
    the_item = db.query(Trades).filter(Trades.user_id == thisuser.id).filter(Trades.id > 0).order_by(
        Trades.id.desc()).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday trade mavjud emas")


