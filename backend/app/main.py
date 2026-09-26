from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Shipping Management System",
    description="API for managing customers, orders, shipments and support tickets.",
    version="0.1.0",
)

class Order(BaseModel):
    order_id: int
    customer_name: str
    destination: str
    weight_kg: float

orders = []

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/orders/")
def get_order():
    return orders

@app.post("/orders")
def create_order(order: Order):
    new_order = {
        "order_id": len(orders) + 1,
        "customer_name": order.customer_name,
        "destination": order.destination,
        "weight_kg": order.weight_kg
    }
    orders.append(new_order)
    return {"message": "Order created successfully", "order": new_order}



@app.get("/")
def root():
    return {
        "message": "Shipping Management System API",
        "version": "0.1.0",
    }