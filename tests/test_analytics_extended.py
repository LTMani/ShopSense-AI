from app.services.analytics.funnel_analytics import ConversionFunnelAnalyzer
from app.services.analytics.market_basket_service import MarketBasketAssociationEngine
from app.services.analytics.retention_cohort_service import CustomerCohortRetentionAnalyzer
from app.services.analytics.stockout_impact_analyzer import StockoutImpactAnalyzer


def test_conversion_funnel_analyzer():
    res = ConversionFunnelAnalyzer.analyze_funnel(
        impressions=10000,
        product_views=1500,
        cart_adds=300,
        checkout_starts=150,
        orders_completed=100
    )

    assert len(res['stages']) == 5
    assert res['overall_conversion_rate'] == 1.0
    assert 'primary_bottleneck' in res
    assert len(res['recommendations']) > 0


def test_market_basket_association_engine():
    baskets = [
        [1, 2, 3],
        [1, 2],
        [1, 3],
        [2, 4],
        [1, 2, 4],
        [1, 5]
    ]

    associated = MarketBasketAssociationEngine.find_associated_products(
        target_product_id=1,
        transaction_baskets=baskets,
        min_support=0.1,
        min_confidence=0.2
    )

    assert len(associated) > 0
    # Item 2 appears frequently with Item 1
    item_2_match = next((x for x in associated if x['product_id'] == 2), None)
    assert item_2_match is not None
    assert item_2_match['lift'] > 0.0


def test_retention_cohort_analyzer():
    orders = [
        {'user_id': 101, 'created_at': '2026-01-10T10:00:00', 'total_amount': 5000.0},
        {'user_id': 101, 'created_at': '2026-02-15T12:00:00', 'total_amount': 3000.0},
        {'user_id': 102, 'created_at': '2026-01-20T14:00:00', 'total_amount': 8000.0},
        {'user_id': 103, 'created_at': '2026-02-05T09:00:00', 'total_amount': 2500.0}
    ]

    cohorts = CustomerCohortRetentionAnalyzer.calculate_monthly_cohorts(orders)
    assert len(cohorts) == 2
    jan_cohort = next(c for c in cohorts if c['cohort_month'] == '2026-01')
    assert jan_cohort['cohort_size'] == 2


def test_stockout_impact_analyzer():
    impact = StockoutImpactAnalyzer.calculate_stockout_loss(
        daily_velocity=2.5,
        unit_sale_price=50000.0,
        unit_cost_price=38000.0,
        stockout_days=10
    )

    assert impact['estimated_lost_units'] == 25.0
    assert impact['estimated_lost_revenue'] == 1250000.0
    assert impact['estimated_lost_profit'] == 300000.0
    assert impact['impact_urgency'] == 'CRITICAL'
