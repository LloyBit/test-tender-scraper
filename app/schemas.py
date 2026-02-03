from pydantic import BaseModel, ConfigDict, Field


class TenderModel(BaseModel):
    """Tender record from rostender.info."""

    model_config = ConfigDict(from_attributes=True)

    number: str
    start_date: str | None = None
    end_date: str | None = None
    title: str | None = None
    url: str | None = None
    region: str | None = None
    price: str | None = None