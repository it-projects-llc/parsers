import argparse
import json
import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_url(dep, arr, date_from):
    return (
        f"https://www.geasar.it/en/flights/all-flights"
        f"?dep={dep}&arr={arr}&date-from={date_from}"
    )


# HTTP GET / return the page content
def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response.text


# Parse HTML / extract flights
def parse_flights(html, date_str, dep, arr):
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
        try:
            # UTC datetime
            dt_local = datetime.strptime(f"{date_str} {dep_time_str}", "%d/%m/%Y %H:%M")
            utc_dt = dt_local.strftime("%Y-%m-%dT%H:%M:00Z")
        except Exception as e:
            logger.warning(f"Datetime error: {e}")
            continue

        flights.append(
            {
                "utc_datetime": utc_dt,
                "flight_number": flight_number,
                "dep": dep,
                "arr": arr,
            }
        )

    return flights


# Command line arguments / run parser / save results
parser = argparse.ArgumentParser()
parser.add_argument("--dep", required=True)
parser.add_argument("--arr", required=True)
parser.add_argument("--date-from", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

url = build_url(args.dep, args.arr, args.date_from)
html = fetch_html(url)
flights = parse_flights(html, args.date_from, args.dep, args.arr)

with open(args.output, "w", encoding="utf-8") as f:
    json.dump(flights, f, ensure_ascii=False, indent=2)

logger.info(f"Saved {len(flights)} flights in {args.output}")
