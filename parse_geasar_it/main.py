import argparse
import json
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROME = ZoneInfo("Europe/Rome")
UTC = ZoneInfo("UTC")


def build_url(dep, arr, date_from):
    return (
        f"https://www.geasar.it/en/flights/all-flights"
        f"?dep={dep}&arr={arr}&date-from={date_from}"
    )


def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response.text


def parse_flights(html, date_obj, dep, arr):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("table.gs-table tbody tr")
    flights = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        flight_number = cols[0].get_text(strip=True)
        departure_info = cols[2].get_text(separator=" ", strip=True)

        dep_time_str = departure_info.split()[-1]

        # Convert local time to UTC
        dt_str = f"{date_obj.strftime('%d/%m/%Y')} {dep_time_str}"
        dt_local = datetime.strptime(dt_str, "%d/%m/%Y %H:%M").replace(tzinfo=ROME)
        dt_utc = dt_local.astimezone(UTC)
        utc_dt = dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

        flights.append(
            {
                "utc_datetime": utc_dt,
                "flight_number": flight_number,
                "dep": dep,
                "arr": arr,
            }
        )

    return flights


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError as err:
        raise argparse.ArgumentTypeError(
            "Invalid date format. Use DD/MM/YYYY (e.g., 18/06/2025)."
        ) from err


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse flights from geasar.it")
    parser.add_argument(
        "--dep", required=True, help="Departure airport code (e.g. OLB)"
    )
    parser.add_argument("--arr", required=True, help="Arrival airport code (e.g. FCO)")
    parser.add_argument(
        "--date-from", required=True, type=parse_date, help="Date (DD/MM/YYYY)"
    )
    parser.add_argument("--output", required=True, help="Path to output JSON file")
    args = parser.parse_args()

    url = build_url(args.dep, args.arr, args.date_from.strftime("%d/%m/%Y"))
    html = fetch_html(url)
    flights = parse_flights(html, args.date_from, args.dep, args.arr)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(flights, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved {len(flights)} flights to {args.output}")
