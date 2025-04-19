from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Product availability at centers
center_products = {
    "C1": ["A", "B", "C"],
    "C2": ["D", "E", "F"],
    "C3": ["G", "H", "I"]
}

# Distance between locations (in km)
distances = {
    ("C1", "L1"): 10,
    ("C2", "L1"): 20,
    ("C3", "L1"): 30,
    ("C1", "C2"): 15,
    ("C1", "C3"): 25,
    ("C2", "C3"): 20,
    ("C2", "C1"): 15,
    ("C3", "C1"): 25,
    ("C3", "C2"): 20,
}

COST_PER_KM = 2

class Order(BaseModel):
    order: Dict[str, int]

def get_cost(path):
    cost = 0
    for i in range(len(path) - 1):
        cost += distances.get((path[i], path[i+1]), 0)
    return cost * COST_PER_KM

def find_min_cost(order: Dict[str, int]) -> int:
    min_cost = float('inf')
    for start_center in ["C1", "C2", "C3"]:
        path = [start_center]
        to_pick = {}
        for product, qty in order.items():
            for center, products in center_products.items():
                if product in products:
                    to_pick.setdefault(center, []).append(product)
                    break
        needed_centers = set(to_pick.keys()) - {start_center}
        for center in needed_centers:
            path.append("L1")
            path.append(center)
        path.append("L1")
        cost = get_cost(path)
        min_cost = min(min_cost, cost)
    return min_cost

@app.post("/calculate-cost")
async def calculate_cost(order: Order):
    cost = find_min_cost(order.order)
    return {"minimum_cost": cost}
