from pydantic import BaseModel, Field
from typing import Optional

class TenderModel(BaseModel):
    number: str = Field(..., description="Номер тендера (уникальный идентификатор)")
    start_date: Optional[str] = Field(None, description="Дата начала тендера")
    end_date: Optional[str] = Field(None, description="Дата окончания тендера")
    title: Optional[str] = Field(None, description="Описание тендера")
    url: Optional[str] = Field(None, description="Ссылка на тендер")
    region: Optional[str] = Field(None, description="Регион проведения тендера")
    price: Optional[str] = Field(None, description="Начальная цена")

    class Config:
        from_attributes = True