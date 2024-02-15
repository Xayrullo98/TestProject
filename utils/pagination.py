from math import ceil

from fastapi import HTTPException


def pagination(form, page, limit):
    return {"current_page": page, "limit": limit, "pages": ceil(form.count() / limit),
            "data": form.offset((page - 1) * limit).limit(limit).all()}


def check_model(db, model, id):
    the_one = db.query(model).filter(model.id == id).first()
    if not the_one:
        raise HTTPException(status_code=400, detail=f"Bazada bunday {model} malumot yo'q!")
    return the_one