from strands import tool
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.tables import Vendor, VendorQuote


class VendorTools:
    """Tools for vendor-related operations."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    @tool
    def search_vendors(self, category: str, service_area: str = None) -> dict:
        """Search for active vendors by category and optional service area.

        Args:
            category: Vendor category (PLUMBING, ELECTRICAL, AC, CLEANING, CARPENTRY, APPLIANCE, INTERNET, GENERAL).
            service_area: Optional area to filter by.

        Returns:
            List of matching vendors sorted by rating.
        """
        db = self.session_factory()
        try:
            query = db.query(Vendor).filter(
                Vendor.category == category.upper(),
                Vendor.status == "ACTIVE",
                Vendor.availability != "UNAVAILABLE",
            )
            if service_area:
                query = query.filter(Vendor.service_area.ilike(f"%{service_area}%"))

            vendors = query.order_by(Vendor.rating.desc()).all()

            return {
                "status": "success",
                "vendors": [
                    {
                        "id": v.id,
                        "name": v.name,
                        "phone": v.phone,
                        "category": v.category,
                        "rating": float(v.rating),
                        "average_cost": float(v.average_cost),
                        "service_area": v.service_area,
                        "availability": v.availability,
                        "total_jobs": v.total_jobs,
                        "successful_jobs": v.successful_jobs,
                    }
                    for v in vendors
                ],
            }
        finally:
            db.close()

    @tool
    def get_vendor_details(self, vendor_id: int) -> dict:
        """Get full details of a vendor.

        Args:
            vendor_id: The vendor's ID.

        Returns:
            Complete vendor information.
        """
        db = self.session_factory()
        try:
            vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
            if not vendor:
                return {"status": "error", "message": f"Vendor {vendor_id} not found"}

            return {
                "status": "success",
                "vendor": {
                    "id": vendor.id,
                    "name": vendor.name,
                    "phone": vendor.phone,
                    "email": vendor.email,
                    "category": vendor.category,
                    "rating": float(vendor.rating),
                    "average_cost": float(vendor.average_cost),
                    "service_area": vendor.service_area,
                    "availability": vendor.availability,
                    "total_jobs": vendor.total_jobs,
                    "successful_jobs": vendor.successful_jobs,
                    "status": vendor.status,
                },
            }
        finally:
            db.close()

    @tool
    def compare_vendor_options(self, vendor_ids: list, complaint_id: int = None) -> dict:
        """Compare multiple vendors side by side for decision making.

        Args:
            vendor_ids: List of vendor IDs to compare.
            complaint_id: Optional complaint ID to get quotes for.

        Returns:
            Comparison of vendors with reasoning.
        """
        db = self.session_factory()
        try:
            vendors = db.query(Vendor).filter(Vendor.id.in_(vendor_ids)).all()
            if not vendors:
                return {"status": "error", "message": "No vendors found"}

            comparison = []
            for v in vendors:
                entry = {
                    "id": v.id,
                    "name": v.name,
                    "rating": float(v.rating),
                    "average_cost": float(v.average_cost),
                    "availability": v.availability,
                    "total_jobs": v.total_jobs,
                    "successful_jobs": v.successful_jobs,
                    "success_rate": round(v.successful_jobs / v.total_jobs * 100, 1) if v.total_jobs > 0 else 0,
                }

                if complaint_id:
                    quote = db.query(VendorQuote).filter(
                        VendorQuote.complaint_id == complaint_id,
                        VendorQuote.vendor_id == v.id,
                    ).first()
                    if quote:
                        entry["quoted_amount"] = float(quote.quoted_amount)
                        entry["estimated_time_minutes"] = quote.estimated_time_minutes

                comparison.append(entry)

            comparison.sort(key=lambda x: (-x["rating"], x["average_cost"]))

            return {
                "status": "success",
                "comparison": comparison,
                "recommendation": comparison[0] if comparison else None,
            }
        finally:
            db.close()

    @tool
    def create_vendor_quote(self, complaint_id: int, vendor_id: int, quoted_amount: float, estimated_time_minutes: int = None, notes: str = None) -> dict:
        """Create a vendor quote for a complaint.

        Args:
            complaint_id: The complaint ID.
            vendor_id: The vendor ID.
            quoted_amount: The quoted price.
            estimated_time_minutes: Estimated time to complete.
            notes: Additional notes.

        Returns:
            Created quote details.
        """
        db = self.session_factory()
        try:
            quote = VendorQuote(
                complaint_id=complaint_id,
                vendor_id=vendor_id,
                quoted_amount=quoted_amount,
                estimated_time_minutes=estimated_time_minutes,
                notes=notes,
                status="RECEIVED",
            )
            db.add(quote)
            db.commit()
            db.refresh(quote)

            return {
                "status": "success",
                "quote": {
                    "id": quote.id,
                    "complaint_id": quote.complaint_id,
                    "vendor_id": quote.vendor_id,
                    "quoted_amount": float(quote.quoted_amount),
                    "status": quote.status,
                },
            }
        finally:
            db.close()
