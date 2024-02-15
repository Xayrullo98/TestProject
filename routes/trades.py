from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user
from schemas.users import UserCurrent

Base.metadata.create_all(bind=engine)

from functions.trades import one_trade, all_trades, create_trade
from schemas.trades import TradeCreate

router_trade = APIRouter()


@router_trade.post('/add', )
def add_user(form: TradeCreate, db: Session = Depends(get_db),
             current_user: UserCurrent = Depends(get_current_active_user)):
    if create_trade(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_trade.get('/', status_code=200)
def get_trades(search: str = None, status: bool = None, id: int = 0, page: int = 1, limit: int = 25,
               db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    if id:
        return one_trade(id, db)
    else:
        return all_trades(search=search, status=status, page=page, limit=limit, db=db, )


@router_trade.get('/user', status_code=200)
def get_user_current(db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if current_user:
        return user_current(current_user, db)
