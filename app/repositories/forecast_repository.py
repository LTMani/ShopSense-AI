from typing import Optional, List
from app.models.forecast import DemandForecast, ForecastEvaluation
from app.repositories.base import BaseRepository


class ForecastRepository(BaseRepository[DemandForecast]):
    def __init__(self):
        super().__init__(DemandForecast)

    def get_latest_by_product(self, product_id: int) -> Optional[DemandForecast]:
        return DemandForecast.query.filter_by(product_id=product_id).order_by(DemandForecast.forecast_date.desc()).first()

    def get_stockout_risks(self, seller_id: Optional[int] = None) -> List[DemandForecast]:
        query = DemandForecast.query.filter_by(stockout_predicted=True)
        if seller_id:
            query = query.filter_by(seller_id=seller_id)
        return query.order_by(DemandForecast.estimated_days_to_stockout.asc()).all()
