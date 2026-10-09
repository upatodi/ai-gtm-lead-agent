"""
Schemas for structured lead information extracted by the LLM.
"""

from typing import Optional

from pydantic import BaseModel, Field


class LeadProfile(BaseModel):
    """
    Structured information extracted from a real estate lead inquiry.
    """

    bedrooms: Optional[int] = Field(default=None)
    property_type: Optional[str] = Field(default=None)
    locations: list[str] = Field(default_factory=list)
    budget_max_lakh: Optional[float] = Field(default=None)
    timeline_months: Optional[float] = Field(default=None)
    wants_to_visit: bool = Field(default=False)