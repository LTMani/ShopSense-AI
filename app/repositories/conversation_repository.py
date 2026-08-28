from typing import Optional, List
from app.models.conversation import Conversation, ConversationMessage, AIInteractionLog
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self):
        super().__init__(Conversation)

    def get_user_conversations(self, user_id: int, copilot_type: str = 'customer_shopping') -> List[Conversation]:
        return Conversation.query.filter_by(
            user_id=user_id,
            copilot_type=copilot_type,
            is_archived=False
        ).order_by(Conversation.updated_at.desc()).all()


class ConversationMessageRepository(BaseRepository[ConversationMessage]):
    def __init__(self):
        super().__init__(ConversationMessage)

    def get_messages(self, conversation_id: int) -> List[ConversationMessage]:
        return ConversationMessage.query.filter_by(conversation_id=conversation_id).order_by(ConversationMessage.created_at.asc()).all()


class AIInteractionLogRepository(BaseRepository[AIInteractionLog]):
    def __init__(self):
        super().__init__(AIInteractionLog)
