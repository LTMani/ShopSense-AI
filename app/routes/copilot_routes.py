from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from app.services.copilot_service import CopilotService
from app.repositories.conversation_repository import ConversationRepository

copilot_bp = Blueprint('copilot_views', __name__)
copilot_api_bp = Blueprint('copilot_api', __name__, url_prefix='/api/copilot')
copilot_service = CopilotService()
conv_repo = ConversationRepository()


@copilot_bp.route('/copilot')
def copilot_page():
    conversations = []
    if current_user.is_authenticated:
        conversations = conv_repo.get_user_conversations(current_user.id, copilot_type='customer_shopping')
    return render_template('copilot/copilot.html', conversations=conversations)


@copilot_api_bp.route('/chat', methods=['POST'])
def api_copilot_chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    conversation_id = data.get('conversation_id')

    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    user_id = current_user.id if current_user.is_authenticated else None

    result = copilot_service.process_message(
        user_id=user_id,
        conversation_id=conversation_id,
        user_message=message
    )
    return jsonify(result)


@copilot_api_bp.route('/conversations/<int:conv_id>', methods=['GET'])
def api_get_conversation(conv_id):
    conv = conv_repo.get_by_id(conv_id)
    if not conv:
        return jsonify({'error': 'Conversation not found'}), 404
    if current_user.is_authenticated and conv.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'conversation': conv.to_dict(include_messages=True)})
