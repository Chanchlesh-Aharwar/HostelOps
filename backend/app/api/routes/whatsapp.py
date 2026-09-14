"""
WhatsApp Webhook - Handles real WhatsApp Business Cloud API messages.
"""

import hashlib
import logging
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from ...database import get_db
from ...config import get_settings
from ...services.whatsapp_service import WhatsAppService, whatsapp_client
from ...services.agent_service import AgentService

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter()


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    """
    Webhook verification endpoint.
    Meta sends this GET request to verify your webhook URL.
    """
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        logger.info("WhatsApp webhook verified successfully")
        return int(hub_challenge)
    else:
        logger.warning("WhatsApp webhook verification failed")
        return {"error": "Verification failed"}


@router.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle incoming WhatsApp messages.
    This receives messages from WhatsApp Business Cloud API.
    """
    data = await request.json()

    # Parse the message
    parsed = whatsapp_client.parse_webhook_message(data)

    if not parsed:
        return {"status": "ignored", "reason": "No message found"}

    phone = parsed["phone"]
    text = parsed["text"]
    media_url = parsed.get("media_url")
    msg_type = parsed.get("type", "TEXT")

    if not text and not media_url:
        return {"status": "ignored", "reason": "Empty message"}

    # Store message and find tenant
    wa_service = WhatsAppService(db)
    result = wa_service.receive_message(phone, text, media_url, msg_type)

    if not result["tenant_found"]:
        # Unknown number - send registration message
        await wa_service.send_message(
            phone,
            "Welcome to HostelOps! Your number is not registered. Please contact your hostel owner."
        )
        return {
            "status": "received",
            "message_id": result["message_id"],
            "tenant_found": False,
        }

    # Process through AI agent
    agent_service = AgentService(db)
    agent_result = agent_service.process_message(text, phone)

    # Send agent response back via WhatsApp
    await wa_service.send_message(phone, agent_result["response"], result.get("tenant_id"))

    # Mark message as processed
    from ...models.tables import Message
    db.query(Message).filter(Message.id == result["message_id"]).update({"processed": 1})
    db.commit()

    return {
        "status": "processed",
        "message_id": result["message_id"],
        "tenant_name": result.get("tenant_name"),
        "agent_response": agent_result["response"],
    }


@router.post("/send")
async def send_message(data: dict, db: Session = Depends(get_db)):
    """Manually send a WhatsApp message."""
    phone = data.get("phone", "")
    text = data.get("text", "")
    tenant_id = data.get("tenant_id")

    if not phone or not text:
        return {"status": "error", "message": "phone and text required"}

    wa_service = WhatsAppService(db)
    result = await wa_service.send_message(phone, text, tenant_id)
    return result


@router.get("/conversation/{tenant_id}")
def get_conversation(tenant_id: int, db: Session = Depends(get_db)):
    """Get WhatsApp conversation history for a tenant."""
    wa_service = WhatsAppService(db)
    messages = wa_service.get_conversation(tenant_id)
    return {"messages": messages}


@router.get("/status")
def whatsapp_status():
    """Check WhatsApp integration status."""
    return {
        "configured": whatsapp_client.is_configured(),
        "phone_number_id": settings.whatsapp_phone_number_id[:10] + "..." if settings.whatsapp_phone_number_id else None,
        "api_version": settings.whatsapp_api_version,
    }
