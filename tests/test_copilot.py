from app.services.copilot_service import CopilotService
from app.models.user import User


def test_copilot_conversational_turn(app):
    with app.app_context():
        user = User.query.filter_by(email='customer@shopsense.ai').first()
        copilot = CopilotService()

        # Turn 1: Initial query
        res1 = copilot.process_message(
            user_id=user.id,
            conversation_id=None,
            user_message="I need a laptop under ₹60,000 for coding, occasional gaming, and long battery life."
        )

        assert res1['conversation_id'] is not None
        assert len(res1['recommended_products']) > 0
        assert res1['extracted_context'].get('budget') == 60000.0
        assert 'Best Match' in [p.get('badge') for p in res1['recommended_products']]

        # Turn 2: Follow-up refinement
        res2 = copilot.process_message(
            user_id=user.id,
            conversation_id=res1['conversation_id'],
            user_message="Battery life matters more than gaming."
        )
        assert res2['conversation_id'] == res1['conversation_id']
        assert 'battery' in res2['extracted_context'].get('priorities', [])
