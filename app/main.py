from fastapi import FastAPI, HTTPException, Request
from prometheus_client import Counter, Histogram, generate_latest
from pydantic import BaseModel
import time
import logging


# -------------------------
# Setup App and Logging
# -------------------------
app = FastAPI(title="DevOps Python API", version="1.0")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
)


# -------------------------
# Metrics
# -------------------------
REQUEST_COUNT = Counter("request_count", "Total API requests")
REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Request latency in seconds"
)


# -------------------------
# Models
# -------------------------
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = 0.0


# -------------------------
# Helper Functions
# -------------------------
def calculate_price_with_tax(price: float, tax: float) -> float:
    return round(price + price * tax, 2)


# -------------------------
# API Endpoints
# -------------------------
@app.get("/")
def read_root():
    logging.info("Root endpoint called")
    return {"message": "Hello, DevOps!"}


@app.get("/health")
def health_check():
    logging.info("Health check called")
    return {"status": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    logging.info(f"Item requested: {item_id}")
    if item_id < 0:
        logging.error(f"Invalid item_id: {item_id}")
        raise HTTPException(status_code=400, detail="Invalid item ID")
    # simulate fetching from DB
    return {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "price": item_id * 10,
    }


@app.post("/items/")
def create_item(item: Item):
    total_price = calculate_price_with_tax(item.price, item.tax)
    logging.info(f"Item created: {item.name} with total_price={total_price}")
    return {"name": item.name, "total_price": total_price}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    logging.info(f"Updating item {item_id} -> {item.name}")
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid item ID")
    total_price = calculate_price_with_tax(item.price, item.tax)
    return {"item_id": item_id, "name": item.name, "total_price": total_price}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    logging.warning(f"Deleting item: {item_id}")
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid item ID")
    return {"status": "deleted", "item_id": item_id}


@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()


@app.get("/trace-example/{user_id}")
def trace_example(user_id: int):
    logging.info(f"Tracing request for user: {user_id}")
    # simulate some business logic
    result = {"user_id": user_id, "message": f"Hello user {user_id}!"}
    return result


@app.get("/sum")
def sum_numbers(a: float, b: float):
    """Simple endpoint to sum two numbers"""
    result = a + b
    logging.info(f"Summing {a} + {b} = {result}")
    return {"result": result}


@app.get("/multiply")
def multiply_numbers(a: float, b: float):
    """Simple endpoint to multiply two numbers"""
    result = a * b
    logging.info(f"Multiplying {a} * {b} = {result}")
    return {"result": result}


@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(duration)
    return response
