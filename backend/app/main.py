from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Order
from app.schemas import OrderCreate, OrderResponse, OrderUpdate


app = FastAPI(
    title="Shipping Management System",
    description="API for managing customers, orders, shipments and support tickets.",
    version="0.1.0",
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Shipping Management System API",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/orders", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order


@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
):
    new_order = Order(
        customer_name=order.customer_name,
        destination=order.destination,
        weight_kg=order.weight_kg,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@app.patch("/orders/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order: OrderUpdate,
    db: Session = Depends(get_db),
):
    existing_order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not existing_order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    if order.customer_name is not None:
        existing_order.customer_name = order.customer_name

    if order.destination is not None:
        existing_order.destination = order.destination

    if order.weight_kg is not None:
        existing_order.weight_kg = order.weight_kg

    if order.status is not None:
        existing_order.status = order.status

    db.commit()
    db.refresh(existing_order)

    return existing_order


@app.delete("/orders/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    existing_order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not existing_order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    db.delete(existing_order)
    db.commit()

    return None