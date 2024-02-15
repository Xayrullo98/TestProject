import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.trades import one_trade
from models.payments import Payments
from utils.pagination import check_model
from utils.pagination import pagination


def all_payments(status, search, start_date, end_date, customer_id, page, limit, db):
    payments = db.query(Payments).options(joinedload(Payments.user),
                                          joinedload(Payments.trade),
                                          )
    if search:
        search_formatted = "%{}%".format(search)
        payments = payments.filter(
            Payments.money.ilike(search_formatted) | Payments.type.ilike(search_formatted))

    if status in [True, False]:
        payments = payments.filter(Payments.status == status)

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
        payments = payments.filter(Payments.created_at >= start_date, Payments.created_at <= end_date)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
    payments = payments.order_by(Payments.id.desc())
    return pagination(payments, page, limit)


def create_payment(form, thisuser, db):
    trade = one_trade(db=db, id=form.trade_id)
    if trade.status:
        raise HTTPException(status_code=200, detail=f"Ushbu savdo tugatilgan")
    new_payment_db = Payments(
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
    the_item = db.query(Payments).options(joinedload(Payments.user),
                                          joinedload(Payments.trade),
                                          ).filter(Payments.id == ident).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday payment mavjud emas")



