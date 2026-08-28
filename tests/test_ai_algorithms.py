import pytest
from app.ai.algorithms.time_series_forecaster import AdvancedTimeSeriesForecaster
from app.ai.algorithms.aspect_sentiment_engine import AspectSentimentExtractionEngine
from app.ai.algorithms.constraint_optimizer import ShoppingMissionConstraintOptimizer
from app.ai.algorithms.rfm_clustering_engine import CustomerRFMClusteringEngine
from app.ai.algorithms.elasticity_pricing_engine import DynamicPricingElasticityEngine


def test_time_series_forecasting_holt_winters():
    # 28 days of daily sales
    sales_history = [
        12.0, 14.0, 15.0, 11.0, 18.0, 24.0, 22.0,
        13.0, 15.0, 16.0, 12.0, 19.0, 25.0, 23.0,
        14.0, 16.0, 17.0, 13.0, 20.0, 27.0, 24.0,
        15.0, 17.0, 18.0, 14.0, 22.0, 29.0, 26.0
    ]

    res = AdvancedTimeSeriesForecaster.holt_winters_forecast(
        series=sales_history,
        season_length=7,
        horizon=14
    )

    assert res['method'] == 'holt_winters_additive'
    assert len(res['forecast_points']) == 14
    for pt in res['forecast_points']:
        assert pt['forecast'] >= 0.0
        assert pt['lower_95'] <= pt['forecast']
        assert pt['upper_95'] >= pt['forecast']


def test_aspect_sentiment_extraction():
    review_text = (
        "The battery life is incredible, easily lasted 14 hours on a single charge! "
        "However, the audio sound was slightly muffled and lack of bass was disappointing. "
        "The build quality is very sturdy and the 120Hz display is super bright."
    )

    res = AspectSentimentExtractionEngine.analyze_aspects_in_text(review_text)
    ratings = res['aspect_ratings']
    
    assert ratings['battery'] >= 85
    assert ratings['sound'] <= 70
    assert ratings['display'] >= 85
    assert len(res['top_praises']) > 0
    assert len(res['top_complaints']) > 0


def test_mission_constraint_optimizer():
    class DummyProduct:
        def __init__(self, id, title, price, rating):
            self.id = id
            self.title = title
            self.sale_price = price
            self.average_rating = rating

    slots = [
        {'role': 'Laptop', 'assigned_budget': 40000.0},
        {'role': 'Desk Chair', 'assigned_budget': 10000.0}
    ]

    candidate_pool = {
        'Laptop': [
            DummyProduct(1, 'Budget Laptop', 38000.0, 4.4),
            DummyProduct(2, 'Premium Laptop', 65000.0, 4.8)
        ],
        'Desk Chair': [
            DummyProduct(3, 'Comfort Chair', 9500.0, 4.6),
            DummyProduct(4, 'High End Chair', 18000.0, 4.9)
        ]
    }

    res = ShoppingMissionConstraintOptimizer.solve_basket(
        slots=slots,
        candidate_pool_by_slot=candidate_pool,
        total_budget=50000.0,
        optimization_mode='balanced'
    )

    assert len(res['items']) == 2
    assert res['allocated_total'] <= 50000.0 * 1.05
    assert res['savings_amount'] >= 0.0


def test_rfm_customer_clustering():
    customers_data = [
        {'user_id': 1, 'name': 'VIP User', 'days_since_last_order': 2, 'order_count': 15, 'total_spent': 85000.0},
        {'user_id': 2, 'name': 'At Risk User', 'days_since_last_order': 65, 'order_count': 8, 'total_spent': 32000.0},
        {'user_id': 3, 'name': 'New User', 'days_since_last_order': 3, 'order_count': 1, 'total_spent': 4500.0}
    ]

    results = CustomerRFMClusteringEngine.calculate_rfm_scores(customers_data)
    assert len(results) == 3
    vip = next(r for r in results if r['user_id'] == 1)
    assert vip['segment'] == 'Champions'


def test_dynamic_pricing_elasticity():
    rec = DynamicPricingElasticityEngine.recommend_optimal_price(
        current_price=20000.0,
        cost_price=12000.0,
        current_stock=25,
        days_without_sale=75
    )

    assert rec['action'] == 'liquidate_markdown'
    assert rec['recommended_price'] < 20000.0
    assert rec['recommended_price'] >= rec['margin_floor']
