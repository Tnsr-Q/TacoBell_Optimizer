## backend/app/main.py

from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest
from pydantic import BaseModel

from backend.optimizer import model, optimizer, store

app = FastAPI(title="Menu Optimizer API", version="0.1.0")

avg_order_savings = Counter("avg_order_savings", "Average savings per order")


@app.get("/healthz", tags=["infra"])
def healthz():
    return {"status": "ok"}


@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), media_type="text/plain")


class HackRequest(BaseModel):
    item_id: str
    zip: str | None = None


class HackResponse(BaseModel):
    data: model.HackResult


@app.post("/v1/hacks", response_model=HackResponse)
def get_hack(req: HackRequest):
    target = store.get_item(req.item_id)
    bases = store.get_bases(req.zip)
    opt = optimizer.Optimizer(
        bases, store.get_addon_costs(req.zip), store.get_special_requests()
    )
    res = opt.hack(target)
    # metric demo – update counter
    if res.savings:
        avg_order_savings.inc(res.savings)
    return {"data": res}
