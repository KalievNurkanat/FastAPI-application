from fastapi import APIRouter
from middlewares.request_counts import request_count_middleware_dispatch

router = APIRouter(
    prefix="/service",
    tags=["Service"]
)


@router.get("/stats")
def get_request_counts():
    return {
        path: {
           "count": stats.count,
           "statuses": dict(stats.statuses_counts)
        }
        for path, stats in request_count_middleware_dispatch.counts.items()
    }