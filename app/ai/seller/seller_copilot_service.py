from typing import Dict, Any, List
from app.ai.gateway import get_ai_gateway
from app.ai.seller.diagnostic_engine import SellerDiagnosticEngine
from app.repositories.product_repository import ProductRepository
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.analytics_repository import ProductPerformanceRepository, SellerMetricDailyRepository


class SellerCopilotService:
    """Answers seller strategic queries grounded in actual database analytics."""

    def __init__(self):
        self.product_repo = ProductRepository()
        self.inventory_repo = InventoryRepository()
        self.performance_repo = ProductPerformanceRepository()
        self.metrics_repo = SellerMetricDailyRepository()

    def process_seller_query(self, seller_id: int, query: str) -> Dict[str, Any]:
        ai_gateway = get_ai_gateway()
        q_lower = query.lower()

        # Find relevant products if mentioned
        products = self.product_repo.get_by_seller(seller_id)
        matched_product = None
        for p in products:
            if p.title.lower() in q_lower or p.brand.lower() in q_lower or (p.category and p.category.name.lower() in q_lower):
                matched_product = p
                break

        if not matched_product and products:
            matched_product = products[0]

        diagnostic_data = None
        if matched_product:
            inv = self.inventory_repo.get_by_product_id(matched_product.id)
            perf = self.performance_repo.find_one_by(product_id=matched_product.id)
            diagnostic_data = SellerDiagnosticEngine.diagnose_product_performance(matched_product, inv, perf)

        # Build diagnostic prompt
        system_prompt = (
            "You are ShopSense Seller AI Copilot, a data-driven retail advisor. "
            "Explain business performance strictly grounded in the seller's actual metrics, inventory levels, and review sentiments."
        )
        context_lines = [f"Seller Query: {query}"]
        if diagnostic_data:
            context_lines.append(f"Product: {diagnostic_data['product_title']}")
            context_lines.append(f"Identified Findings: {'; '.join(diagnostic_data['findings'])}")
            context_lines.append(f"Action Recommendations: {'; '.join(diagnostic_data['recommendations'])}")

        context_prompt = "\n".join(context_lines)
        ai_response = ai_gateway.generate(context_prompt, system_prompt=system_prompt)

        return {
            'query': query,
            'response': ai_response['content'],
            'diagnostic': diagnostic_data,
            'latency_ms': ai_response.get('latency_ms', 0)
        }
