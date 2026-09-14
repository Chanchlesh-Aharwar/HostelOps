"""
Image Service - Analyze complaint images using Amazon Bedrock Vision.
Falls back to mock analysis when AWS credentials are not available.
"""

import json
import logging
import os
from pathlib import Path

from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE_MB = 10


def analyze_complaint_image(image_path: str, complaint_text: str = "") -> dict:
    """
    Analyze a complaint image using Bedrock Vision API.
    Returns structured analysis of the image.
    """
    if not settings.aws_access_key_id or not settings.aws_secret_access_key:
        return _mock_analyze(image_path, complaint_text)

    try:
        import boto3
        from pathlib import Path

        bedrock = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

        image_data = Path(image_path).read_bytes()
        import base64
        image_b64 = base64.b64encode(image_data).decode("utf-8")

        prompt = f"""Analyze this maintenance complaint image for a hostel/PG property.

Context from tenant: {complaint_text}

Provide a JSON analysis with these fields:
- category: One of PLUMBING, ELECTRICAL, AC, CLEANING, FURNITURE, INTERNET, APPLIANCE, SECURITY, OTHER
- possible_issue: Brief description of what you see
- severity: LOW, MEDIUM, HIGH, or URGENT
- confidence: 0.0 to 1.0
- details: Any additional observations

Return ONLY valid JSON, no other text."""

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            messages: [{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }],
        })

        response = bedrock.invoke_model(
            modelId="anthropic.claude-sonnet-4-20250514-v1:0",
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        result = json.loads(response["body"].read())
        text = result["content"][0]["text"]

        # Extract JSON from response
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        analysis = json.loads(text.strip())
        analysis["source"] = "bedrock_vision"
        return analysis

    except Exception as e:
        logger.error(f"Vision analysis failed: {e}")
        return _mock_analyze(image_path, complaint_text)


def _mock_analyze(image_path: str, complaint_text: str = "") -> dict:
    """Mock analysis when Bedrock is not available."""
    text_lower = complaint_text.lower()

    category = "OTHER"
    possible_issue = "Issue detected from image"
    severity = "MEDIUM"

    if any(w in text_lower for w in ["tap", "leak", "pipe", "plumb", "bathroom", "water"]):
        category = "PLUMBING"
        possible_issue = "Water leakage or plumbing issue"
        severity = "HIGH"
    elif any(w in text_lower for w in ["electric", "wire", "switch", "light", "fan"]):
        category = "ELECTRICAL"
        possible_issue = "Electrical fixture issue"
        severity = "MEDIUM"
    elif any(w in text_lower for w in ["ac", "cool", "air"]):
        category = "AC"
        possible_issue = "AC or cooling system issue"
        severity = "MEDIUM"
    elif any(w in text_lower for w in ["clean", "dirt", "mess"]):
        category = "CLEANING"
        possible_issue = "Cleaning required"
        severity = "LOW"
    elif any(w in text_lower for w in ["furniture", "bed", "table", "chair"]):
        category = "FURNITURE"
        possible_issue = "Furniture damage"
        severity = "MEDIUM"

    return {
        "category": category,
        "possible_issue": possible_issue,
        "severity": severity,
        "confidence": 0.75,
        "details": f"Mock analysis based on text context: {complaint_text[:100]}",
        "source": "mock_vision",
    }


def save_upload(file_content: bytes, filename: str, content_type: str) -> str:
    """Save an uploaded file and return the path."""
    import uuid

    ext = filename.split(".")[-1] if "." in filename else "bin"
    unique_name = f"{uuid.uuid4()}.{ext}"
    file_path = UPLOAD_DIR / unique_name

    file_path.write_bytes(file_content)
    return str(file_path)
