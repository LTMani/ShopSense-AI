from datetime import datetime, timezone
import json
from typing import Dict, Any, Optional
from app.models.tracking import BrowsingEvent, SearchHistory
from app.extensions import db


class TelemetryTracker:
    """Logs fine-grained behavioral interactions and searches for personalization and funnel analytics."""

    @staticmethod
    def track_interaction(
        user_id: Optional[int],
        session_id: str,
        event_type: str,
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        dwell_time: int = 0,
        metadata_dict: Optional[Dict[str, Any]] = None
    ) -> None:
        try:
            interaction = BrowsingEvent(
                user_id=user_id,
                session_id=session_id,
                event_type=event_type,
                product_id=product_id,
                category_id=category_id,
                dwell_time_seconds=dwell_time,
                metadata_payload=json.dumps(metadata_dict or {})
            )
            db.session.add(interaction)
            db.session.commit()
        except Exception:
            db.session.rollback()

    @staticmethod
    def log_search(
        user_id: Optional[int],
        session_id: str,
        query_text: str,
        results_count: int,
        extracted_entities: Optional[Dict[str, Any]] = None,
        clicked_product_id: Optional[int] = None
    ) -> None:
        try:
            log_entry = SearchHistory(
                user_id=user_id,
                session_id=session_id,
                query_text=query_text,
                results_count=results_count,
                extracted_entities=json.dumps(extracted_entities or {}),
                clicked_product_id=clicked_product_id
            )
            db.session.add(log_entry)
            db.session.commit()
        except Exception:
            db.session.rollback()
