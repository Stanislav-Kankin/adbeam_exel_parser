from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse

import httpx
import tldextract
from selectolax.parser import HTMLParser
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from adbeam_excel_parser.models import SiteAuditResult, SiteFitStatus, SiteSignals

REQUEST_TIMEOUT_SECONDS = 12.0
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}

POSITIVE_CATALOG_TERMS = (
    "каталог",
    "товар",
    "продукц",
    "интернет-магазин",
    "магазин",
    "catalog",
    "shop",
    "product",
)
POSITIVE_CART_TERMS = ("корзин", "в корзину", "cart", "basket")
POSITIVE_BUY_TERMS = ("купить", "оформить заказ", "заказать онлайн", "buy now")
POSITIVE_DELIVERY_TERMS = ("доставк", "самовывоз", "delivery", "shipping")
POSITIVE_PAYMENT_TERMS = ("оплат", "visa", "mastercard", "mir", "payment")
POSITIVE_CONSUMER_TERMS = (
    "в наличии",
    "акция",
    "скидк",
    "новинки",
    "заказ онлайн",
    "быстрый заказ",
    "оформить заказ",
    "доставка по",
)
NEGATIVE_REQUEST_ONLY_TERMS = (
    "оставить заявку",
    "запросить кп",
    "коммерческ",
    "связаться с менеджером",
    "получить консультацию",
)
NEGATIVE_B2B_TERMS = (
    "оптов",
    "для дилеров",
    "производство",
    "промышлен",
    "корпоративн",
    "b2b",
)
HACKED_TERMS = (
    "casino",
    "viagra",
    "porn",
    "sex",
    "slot",
    "betting",
    "казино",
    "порно",
)
PRICE_PATTERN = re.compile(r"\d[\d\s]{0,12}(?:₽|руб\.?|рублей)", flags=re.IGNORECASE)


@dataclass(slots=True)
class FetchedPage:
    requested_url: str
    final_url: str
    status_code: int
    html: str


def audit_website_url(url: str | None, company_name: str | None = None, row_index: int = 0) -> SiteAuditResult:
    normalized_url = normalize_url(url)
    if not normalized_url:
        return SiteAuditResult(
            row_index=row_index,
            company_name=company_name,
            original_url=url,
            normalized_url=None,
            final_url=None,
            domain=None,
            title=None,
            http_status=None,
            status=SiteFitStatus.NO_SITE,
            status_reason="В строке нет корректного сайта.",
            error=None,
        )

    try:
        page = fetch_page(normalized_url)
    except Exception as exc:
        return SiteAuditResult(
            row_index=row_index,
            company_name=company_name,
            original_url=url,
            normalized_url=normalized_url,
            final_url=None,
            domain=extract_domain(normalized_url),
            title=None,
            http_status=None,
            status=SiteFitStatus.BROKEN,
            status_reason="Сайт не удалось загрузить.",
            error=str(exc),
        )

    if page.status_code >= 400:
        return SiteAuditResult(
            row_index=row_index,
            company_name=company_name,
            original_url=url,
            normalized_url=normalized_url,
            final_url=page.final_url,
            domain=extract_domain(page.final_url),
            title=extract_title(page.html),
            http_status=page.status_code,
            status=SiteFitStatus.BROKEN,
            status_reason=f"HTTP {page.status_code}",
            error=None,
        )

    title = extract_title(page.html)
    signals = extract_signals(page.html)
    status, reason = classify_signals(signals)

    return SiteAuditResult(
        row_index=row_index,
        company_name=company_name,
        original_url=url,
        normalized_url=normalized_url,
        final_url=page.final_url,
        domain=extract_domain(page.final_url),
        title=title,
        http_status=page.status_code,
        status=status,
        status_reason=reason,
        signals=signals,
        error=None,
    )


@retry(
    stop=stop_after_attempt(2),
    wait=wait_fixed(1),
    retry=retry_if_exception_type(httpx.HTTPError),
    reraise=True,
)
def fetch_page(url: str) -> FetchedPage:
    with httpx.Client(
        follow_redirects=True,
        timeout=REQUEST_TIMEOUT_SECONDS,
        headers=DEFAULT_HEADERS,
    ) as client:
        response = client.get(url)
        response.raise_for_status()
        return FetchedPage(
            requested_url=url,
            final_url=str(response.url),
            status_code=response.status_code,
            html=response.text,
        )


def extract_title(html: str) -> str | None:
    if not html:
        return None

    parser = HTMLParser(html)
    title_node = parser.css_first("title")
    if title_node is None:
        return None

    title = title_node.text(strip=True)
    return title or None


def extract_signals(html: str) -> SiteSignals:
    if not html:
        return SiteSignals()

    parser = HTMLParser(html)
    text = parser.body.text(separator=" ", strip=True) if parser.body else parser.text(separator=" ", strip=True)
    text_lower = compact_text(text).lower()
    html_lower = html.lower()

    hacked_terms = find_present_terms(text_lower, HACKED_TERMS)

    return SiteSignals(
        has_catalog=contains_any(text_lower, POSITIVE_CATALOG_TERMS) or contains_any(html_lower, ("/catalog", "/catalogue", "/shop", "/products")),
        has_cart=contains_any(text_lower, POSITIVE_CART_TERMS) or contains_any(html_lower, ("cart", "basket")),
        has_buy_button=contains_any(text_lower, POSITIVE_BUY_TERMS),
        has_price=bool(PRICE_PATTERN.search(text_lower)) or "₽" in html or "руб" in text_lower,
        has_delivery=contains_any(text_lower, POSITIVE_DELIVERY_TERMS),
        has_payment=contains_any(text_lower, POSITIVE_PAYMENT_TERMS),
        has_consumer_language=contains_any(text_lower, POSITIVE_CONSUMER_TERMS),
        request_only=contains_any(text_lower, NEGATIVE_REQUEST_ONLY_TERMS),
        has_b2b_language=contains_any(text_lower, NEGATIVE_B2B_TERMS),
        hacked_terms=hacked_terms,
    )


def classify_signals(signals: SiteSignals) -> tuple[SiteFitStatus, str]:
    if signals.hacked_terms:
        return SiteFitStatus.HACKED, f"Найдены подозрительные слова: {', '.join(signals.hacked_terms)}"

    strong_direct = signals.has_cart or signals.has_buy_button or signals.has_price
    positive_score = sum(
        (
            signals.has_catalog,
            signals.has_cart,
            signals.has_buy_button,
            signals.has_price,
            signals.has_delivery,
            signals.has_payment,
            signals.has_consumer_language,
        )
    )

    if positive_score >= 4 and strong_direct and not signals.request_only:
        return SiteFitStatus.FIT_NOW, "Есть явные direct/ecom сигналы."

    if positive_score >= 2 and not (signals.request_only and not strong_direct):
        return SiteFitStatus.FIT_LATER, "Есть часть сигналов, но direct-механика слабая или неполная."

    if signals.request_only or (signals.has_b2b_language and not strong_direct):
        return SiteFitStatus.NOT_FIT, "Сайт больше похож на B2B/leadgen без прямой покупки."

    return SiteFitStatus.NOT_FIT, "Недостаточно direct/ecom сигналов."


def normalize_url(raw_url: str | None) -> str | None:
    if raw_url is None:
        return None

    value = raw_url.strip()
    if not value:
        return None

    if not value.startswith(("http://", "https://")):
        value = f"https://{value}"

    parsed = urlparse(value)
    if not parsed.netloc:
        return None

    return value


def extract_domain(url: str | None) -> str | None:
    if not url:
        return None

    extracted = tldextract.extract(url)
    if not extracted.domain:
        return None

    if extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}"

    return extracted.domain


def compact_text(value: str) -> str:
    return " ".join(value.split())


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def find_present_terms(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if term in text]
