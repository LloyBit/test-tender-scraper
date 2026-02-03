"""HTML parser for rostender.info tender listings."""

from bs4 import BeautifulSoup
from app.schemas import TenderModel


class RostenderParser:
    """Parses tender HTML blocks into TenderModel instances."""

    ROW_SELECTOR = "article.tender-row.row"
    ITEMS_PER_PAGE = 20

    @staticmethod
    def parse_tender(element) -> TenderModel | None:
        """Extract one tender from a BS4 element. Returns None if number is missing."""
        number_tag = element.find("span", class_="tender__number")
        number_text = number_tag.get_text(strip=True) if number_tag else ""
        number = number_text.split("№")[-1].strip() if "№" in number_text else None
        if not number:
            return None

        start_el = element.find("span", class_="tender__date-start")
        start_date = start_el.get_text(strip=True).replace("от ", "") if start_el else None

        end_el = element.select_one("span.tender__date-end, span.black")
        end_date = end_el.get_text(strip=True) if end_el else None

        desc = element.find("a", class_="description")
        title = desc.get_text(strip=True) if desc else None
        href = desc.get("href", "") if desc else ""
        region_part = href.split("/")[2] if len(href.split("/")) > 2 else None
        url = f"https://rostender.info/region/{region_part}/{number}" if region_part else None

        price_el = element.find("div", class_="starting-price--price")
        price = price_el.get_text(strip=True) if price_el else None

        region_el = element.find("div", class_="tender-address")
        region = region_el.get_text(strip=True) if region_el else None

        return TenderModel(
            number=number,
            start_date=start_date,
            end_date=end_date,
            title=title,
            url=url,
            region=region,
            price=price,
        )

    def parse_document(self, html: str) -> list[TenderModel]:
        """Parse a full page HTML and return list of tenders."""
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select(self.ROW_SELECTOR)
        result = []
        for row in rows:
            tender = self.parse_tender(row)
            if tender:
                result.append(tender)
        return result
