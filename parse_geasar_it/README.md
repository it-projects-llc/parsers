# Geasar.it Flight Scraper

This Python script scrapes flight information from the
[Geasar.it](https://www.geasar.it/en/flights/all-flights) website and outputs the data
as JSON.

## Features

- Scrapes flight data by departure airport, arrival airport, and date.
- Parses flight number and UTC datetime.
- Outputs a JSON file with structured flight data.

## Requirements

- Python 3.7+
- Dependencies:
  - requests
  - beautifulsoup4

pip3 install requests beautifulsoup4

## Usage

- python3 main.py --dep OLB --arr FCO --date-from 05/06/2025 --output flights.json

- Arguments: --dep – Departure airport code (e.g. OLB) --arr – Arrival airport code
  (e.g. FCO) --date-from – Date in format DD/MM/YYYY (e.g. 05/06/2025) --output – Output
  file name +.json (e.g. flights.json)
