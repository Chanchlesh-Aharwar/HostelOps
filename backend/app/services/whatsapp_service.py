"""
WhatsApp Business Cloud API Service.
Handles sending and receiving WhatsApp messages via Meta's Cloud API.
"""

import json
import logging
from typing import Optional

import httpx
from sqlalchemy.orm import Session

from ..config import get_settings
from ..models.tables import Message, Tenant

logger = logging.getLogger(__name__)
settings = get_settings()


class WhatsAppCloudAPI:
    """WhatsApp Business Cloud API client."""

    def __init__(self):
        self.phone_number_id = settings.whatsapp_phone_number_id
        self.access_token = settings.whatsapp_access_token
        self.api_url = settings.whatsapp_api_url

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def is_configured(self) -> bool:
        """Check if WhatsApp is properly configured."""
        return bool(self.phone_number_id and self.access_token)

    async def send_text_message(self, to: str, text: str) -> dict:
        """Send a text message via WhatsApp."""
        if not self.is_configured():
            logger.warning("WhatsApp not configured, message not sent")
            return {"status": "not_configured", "message": "WhatsApp not configured"}

        url = f"{self.api_url}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text},
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self.headers, timeout=30)
                result = response.json()

                if response.status_code == 200:
                    logger.info(f"WhatsApp message sent to {to}")
                    return {"status": "success", "message_id": result.get("messages", [{}])[0].get("id")}
                else:
                    logger.error(f"WhatsApp API error: {result}")
                    return {"status": "error", "error": result}

        except Exception as e:
            logger.error(f"WhatsApp send error: {e}")
            return {"status": "error", "error": str(e)}

    async def send_interactive_message(self, to: str, text: str, buttons: list[dict]) -> dict:
        """Send a message with buttons."""
        if not self.is_configured():
            return {"status": "not_configured"}

        url = f"{self.api_url}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {"buttons": buttons},
            },
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self.headers, timeout=30)
                return response.json()
        except Exception as e:
            logger.error(f"WhatsApp interactive message error: {e}")
            return {"status": "error", "error": str(e)}

    def parse_webhook_message(self, data: dict) -> Optional[dict]:
        """Parse incoming WhatsApp webhook message."""
        try:
            entry = data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})

            messages = value.get("messages", [])
            if not messages:
                return None

            message = messages[0]
            phone = message.get("from", "")
            msg_type = message.get("type", "")

            text = ""
            media_url = None

            if msg_type == "text":
                text = message.get("text", {}).get("body", "")
            elif msg_type == "image":
                media_url = message.get("image", {}).get("id")
                text = message.get("image", {}).get("caption", "")
            elif msg_type == "document":
                media_url = message.get("document", {}).get("id")

            return {
                "phone": phone,
                "text": text,
                "type": msg_type,
                "media_url": media_url,
                "message_id": message.get("id"),
                "timestamp": message.get("timestamp"),
            }

        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing webhook: {e}")
            return None


whatsapp_client = WhatsAppCloudAPI()


class WhatsAppService:
    """WhatsApp message handling service."""

    def __init__(self, db: Session):
        self.db = db

    def receive_message(self, phone: str, text: str, media_url: str = None, msg_type: str = "TEXT") -> dict:
        """Process incoming WhatsApp message."""
        tenant = self.db.query(Tenant).filter(
            Tenant.phone == phone,
            Tenant.status == "ACTIVE",
        ).first()

        message = Message(
            tenant_id=tenant.id if tenant else None,
            direction="INBOUND",
            channel="WHATSAPP",
            message_type=msg_type,
            message_text=text,
            media_url=media_url,
            processed=0,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return {
            "status": "success",
            "message_id": message.id,
            "tenant_found": tenant is not None,
            "tenant_id": tenant.id if tenant else None,
            "tenant_name": tenant.name if tenant else None,
        }

    async def send_message(self, phone: str, text: str, tenant_id: int = None) -> dict:
        """Send a WhatsApp message."""
        result = await whatsapp_client.send_text_message(phone, text)

        message = Message(
            tenant_id=tenant_id,
            direction="OUTBOUND",
            channel="WHATSAPP",
            message_type="TEXT",
            message_text=text,
            processed=1,
        )
        self.db.add(message)
        self.db.commit()

        return {
            "status": "sent" if result.get("status") == "success" else "failed",
            "message_id": message.id,
            "whatsapp_result": result,
        }

    def get_conversation(self, tenant_id: int, limit: int = 20) -> list:
        """Get WhatsApp conversation history for a tenant."""
        messages = self.db.query(Message).filter(
            Message.tenant_id == tenant_id,
            Message.channel == "WHATSAPP",
        ).order_by(Message.created_at.desc()).limit(limit).all()

        return [
            {
                "id": m.id,
                "direction": m.direction,
                "message_text": m.message_text,
                "message_type": m.message_type,
                "media_url": m.media_url,
                "created_at": str(m.created_at) if m.created_at else None,
            }
            for m in reversed(messages)
        ]
