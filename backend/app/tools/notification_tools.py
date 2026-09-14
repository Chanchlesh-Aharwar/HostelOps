from strands import tool
from sqlalchemy.orm import Session
from datetime import datetime

from ..models.tables import Message, AgentAction


class NotificationTools:
    """Tools for notifications and agent action logging."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    @tool
    def send_notification(self, tenant_id: int, message: str, channel: str = "WEB") -> dict:
        """Send a notification to a tenant.

        Args:
            tenant_id: The tenant to notify.
            message: The notification message.
            channel: Channel to send through (WEB, WHATSAPP, PHONE, SYSTEM).

        Returns:
            Notification status.
        """
        db = self.session_factory()
        try:
            msg = Message(
                tenant_id=tenant_id,
                direction="OUTBOUND",
                channel=channel.upper(),
                message_type="TEXT",
                message_text=message,
                processed=1,
            )
            db.add(msg)
            db.commit()
            db.refresh(msg)

            return {
                "status": "success",
                "message_id": msg.id,
                "channel": channel,
                "message": f"Notification sent to tenant {tenant_id}: {message}",
            }
        finally:
            db.close()

    @tool
    def log_agent_action(self, agent_name: str, action_type: str, entity_type: str = None, entity_id: int = None, input_data: dict = None, output_data: dict = None, status: str = "SUCCESS", error_message: str = None) -> dict:
        """Log an agent action for audit trail.

        Args:
            agent_name: Name of the agent performing the action.
            action_type: Type of action (e.g., CLASSIFY_COMPLAINT, SEARCH_VENDORS).
            entity_type: Type of entity affected (e.g., COMPLAINT, VENDOR).
            entity_id: ID of the entity affected.
            input_data: Input data for the action as JSON.
            output_data: Output/result of the action as JSON.
            status: Status of the action (STARTED, SUCCESS, FAILED, WAITING_APPROVAL).
            error_message: Error message if failed.

        Returns:
            Logged action details.
        """
        db = self.session_factory()
        try:
            action = AgentAction(
                agent_name=agent_name,
                action_type=action_type,
                entity_type=entity_type,
                entity_id=entity_id,
                input_data=input_data,
                output_data=output_data,
                status=status,
                error_message=error_message,
                completed_at=datetime.now() if status in ["SUCCESS", "FAILED"] else None,
            )
            db.add(action)
            db.commit()
            db.refresh(action)

            return {
                "status": "success",
                "action_id": action.id,
                "agent_name": agent_name,
                "action_type": action_type,
                "status": status,
            }
        finally:
            db.close()
