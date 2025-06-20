
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/it-projects-llc/parsers/actions/workflows/pre-commit.yml/badge.svg?branch=master)](https://github.com/it-projects-llc/parsers/actions/workflows/pre-commit.yml?query=branch%3Amaster)
[![Build Status](https://github.com/it-projects-llc/parsers/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/it-projects-llc/parsers/actions/workflows/test.yml?query=branch%3Amaster)
[![codecov](https://codecov.io/gh/it-projects-llc/parsers/branch/master/graph/badge.svg)](https://codecov.io/gh/it-projects-llc/parsers)
<!-- /!\ Non OCA Context : Set here the badge of your translation instance. -->

<!-- /!\ do not modify above this line -->

# Booking.com Hotel Scraper (Italy - Sardinia & Calabria)

This Python script scrapes hotel data from [Booking.com](https://www.booking.com) using their internal GraphQL API. It collects hotels from the Sardinia and Calabria regions and saves them in a `result.csv` file.

## Features

- Scrapes hotel `id`, `name`, `city`, and `address`
- Adds constant fields: `state_id=base.it`, `is_hotel=1`, `is_company=1`
- Handles pagination
- Avoids duplicates

## Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install requests
```
## Usage

 - Clone the repository
 - Set maximum number of hotels to scrape in main.py, line 34:
		maximum_hotels = 1000  # Set your desired hotel count limit
 - Run the script:
	python3 main.py
 - Output will be saved as result.csv.

## Output Format

id,name,city,address,state_id,is_hotel,is_company
123456,Hotel Roma,Rome,Via Nazionale 1,base.it,1,1

## Notes

This script uses internal (unofficial) Booking.com GraphQL API and may stop working if the site structure changes.
Use responsibly to avoid temporary IP bans. Includes a delay between requests.



<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

This part will be replaced when running the oca-gen-addons-table script from OCA/maintainer-tools.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [LGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to IT-Projects LLC
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
<!-- /!\ Non OCA Context : Set here the full description of your organization. -->
