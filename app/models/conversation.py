from datetime import datetime, timezone
import json
from app.extensions import db


class Conversation(db.Model):
    """Chat session for AI Customer Shopping Copilot or Seller Intelligence Copilot."""
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
    copilot_type = db.Column(db.String(30), default='customer_shopping', nullable=False, index=True)
    session_title = db.Column(db.String(150), default='New Shopping Assistant Session', nullable=False)
    context_state = db.Column(db.Text, nullable=True, default='{}')
    is_archived = db.Column(db.Boolean, default=False, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='conversations')
    messages = db.relationship('ConversationMessage', back_populates='conversation', cascade='all, delete-orphan', lazy='dynamic')

    def get_context_dict(self):
        try:
            return json.loads(self.context_state or '{}')
        except Exception:
            return {}

    def set_context_dict(self, context_dict):
        self.context_state = json.dumps(context_dict if isinstance(context_dict, dict) else {})

    def to_dict(self, include_messages=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'copilot_type': self.copilot_type,
            'session_title': self.session_title,
            'context': self.get_context_dict(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_messages:
            data['messages'] = [m.to_dict() for m in self.messages.order_by(ConversationMessage.created_at.asc()).all()]
        return data


class ConversationMessage(db.Model):
    """Single message entry in AI conversation with structured recommendation payload."""
    __tablename__ = 'conversation_messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False, index=True)
    sender = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    extracted_requirements = db.Column(db.Text, nullable=True, default='{}')
    recommended_product_ids = db.Column(db.Text, nullable=True, default='[]')
    explanation_text = db.Column(db.Text, nullable=True)
    confidence_score = db.Column(db.Float, default=1.0, nullable=False)
    latency_ms = db.Column(db.Integer, default=0, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    conversation = db.relationship('Conversation', back_populates='messages')

    def get_extracted_requirements_dict(self):
        try:
            return json.loads(self.extracted_requirements or '{}')
        except Exception:
            return {}

    def get_recommended_product_ids_list(self):
        try:
            return json.loads(self.recommended_product_ids or '[]')
        except Exception:
            return []

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender': self.sender,
            'content': self.content,
            'extracted_requirements': self.get_extracted_requirements_dict(),
            'recommended_product_ids': self.get_recommended_product_ids_list(),
            'explanation_text': self.explanation_text,
            'confidence_score': round(self.confidence_score or 1.0, 2),
            'latency_ms': self.latency_ms,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AIInteractionLog(db.Model):
    """Audit log for telemetry on AI latency, token usage, model accuracy, and fallback rates."""
    __tablename__ = 'ai_interaction_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    feature = db.Column(db.String(60), nullable=False, index=True)
    provider = db.Column(db.String(40), nullable=False)
    model_name = db.Column(db.String(80), nullable=False)
    prompt_tokens = db.Column(db.Integer, default=0, nullable=False)
    completion_tokens = db.Column(db.Integer, default=0, nullable=False)
    latency_ms = db.Column(db.Integer, default=0, nullable=False)
    success = db.Column(db.Boolean, default=True, nullable=False)
    error_message = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
