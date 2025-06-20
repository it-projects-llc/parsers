import copy
import csv
import json
import logging
import time

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = "https://www.booking.com/dml/graphql?ss=Italy" "&lang=en-us&aid=304142"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Content-Type": "application/json",
    "Referer": "https://www.booking.com/searchresults.html?region=908",
    "x-booking-csrf-token": (
        "eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJjb250ZXh0LWVucmljaG1lbnQtYXBpIiwic3"
        "ViIjoiY3NyZi10b2tlbiIsImlhdCI6MTc1MDM2NzM3NSwiZXhwIjoxNzUwNDUzNzc1fQ."
        "1mpLQoicPHNU-p3a9XLxVrqlTQjNK4BmyVcR-HOL81Mt_dsAxAkLDulrTwGa42XBqnp1pfnNIguXKSKTNbBIXQ"
    ),
    "x-booking-pageview-id": "d82194c7b1470608",
    "apollographql-client-name": "b-search-web-searchresults_rust",
    "x-booking-context-action-name": "searchresults_irene",
    "x-booking-context-aid": "304142",
    "x-booking-dml-cluster": "rust",
    "x-booking-site-type-id": "1",
    "x-booking-topic": "capla_browser_b-search-web-searchresults",
}

cookies = {"bkng": ""}

with open("booking_query_payload.json", encoding="utf-8") as f:
    base_payload = json.load(f)

regions = [
    {"name": "Sardinia", "destId": 908},
    {"name": "Calabria", "destId": 897},
]

maximum_hotels = 10000
csv_rows = []
seen_ids = set()

for region in regions:
    logger.info("Processing %s", region["name"])
    for offset in range(0, maximum_hotels, 25):
        logger.info("Loading hotels offset = %s", offset)

        payload = copy.deepcopy(base_payload)
        payload["variables"]["input"]["pagination"]["offset"] = offset
        payload["variables"]["input"]["location"]["destId"] = region["destId"]
        payload["variables"]["input"]["location"]["destType"] = "REGION"

        try:
            response = requests.post(
                url,
                headers=headers,
                cookies=cookies,
                json=payload,
                timeout=10,
            )
        except requests.exceptions.RequestException as e:
            logger.error("Request failed: %s", e)
            break

        if response.status_code != 200:
            logger.error("HTTP error %s at offset %s", response.status_code, offset)
            break

        try:
            data = response.json()
            hotels = data["data"]["searchQueries"]["search"]["results"]

            if not hotels:
                logger.info("No more results.")
                break

            for hotel in hotels:
                try:
                    hotel_id = hotel["basicPropertyData"]["id"]
                    if hotel_id in seen_ids:
                        continue

                    name = hotel.get("displayName", {}).get("text", "")
                    city = (
                        hotel["basicPropertyData"].get("location", {}).get("city", "")
                    )
                    address = (
                        hotel["basicPropertyData"]
                        .get("location", {})
                        .get("address", "")
                    )

                    csv_rows.append(
                        [
                            hotel_id,
                            name.replace(",", " ").strip(),
                            city.replace(",", " ").strip(),
                            address.replace(",", " ").strip(),
                            "base.it",
                            "1",
                            "1",
                        ]
                    )
                    seen_ids.add(hotel_id)
                except Exception as e:
                    logger.warning("Hotel parse error: %s", e)
        except Exception as e:
            logger.error("JSON parse error at offset %s: %s", offset, e)
            logger.debug(response.text[:500])
            break

        time.sleep(1.5)

with open("result.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        [
            "id",
            "name",
            "city",
            "address",
            "state_id",
            "is_hotel",
            "is_company",
        ]
    )
    writer.writerows(csv_rows)

logger.info("Saved %d unique hotels to 'result.csv'", len(csv_rows))
