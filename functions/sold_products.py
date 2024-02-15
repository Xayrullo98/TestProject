import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.sold_products import Sold_Products
from utils.pagination import pagination


def all_sold_products(status, search, start_date, end_date, customer_id, page, limit, db):
    sold_products = db.query(Sold_Products).options(joinedload(Sold_Products.user),
                                                    joinedload(Sold_Products.trade),
                                                    )
    if search:
        search_formatted = "%{}%".format(search)
        sold_products = sold_products.filter(
            Sold_Products.money.ilike(search_formatted) | Sold_Products.type.ilike(search_formatted))

    if status in [True, False]:
        sold_products = sold_products.filter(Sold_Products.status == status)

    if customer_id:
        sold_products = sold_products.filter(Sold_Products.customer_id == customer_id)

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
        sold_products = sold_products.filter(Sold_Products.created_at >= start_date,
                                             Sold_Products.created_at <= end_date)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
    sold_products = sold_products.order_by(Sold_Products.id.desc())
    return pagination(sold_products, page, limit)


def one_sold_products(db, id):
    the_item = db.query(Sold_Products).options(joinedload(Sold_Products.user),
                                               joinedload(Sold_Products.trade),
                                               ).filter(Sold_Products.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday sold_products mavjud emas")
