# AlkoReviewScraper

## Overview

**AlkoReviewScraper** provides two web scrapers that collect cummunity rating data for rums and whiskeys from two different websites websites: [The Rum Howler Blog](https://therumhowlerblog.com/rum-reviews/), [WhiskyScores.com](https://whiskyscores.com)
These two webscrapers were created for gathering review data to use in one of my other projects: [ BudgetBarshelf ](https://github.com/oskuuh43/alko_app/tree/main) - an application that helps users make better spirit purchases based on product ratings and price.

##  How To run

1. Clone this repository.
2. Ensure you have Python installed.
3. Install the required libraries:

   ```bash
   pip install -r requirements.txt

4. Run the scrapers:

   ```bash
   # Run the rum scraper
   python rum_scraper.py

   # Run the whiskey scraper
   python whiskey_scraper.py

Each script will print progress and save data into the `data/` directory.

## Sources

- [therumhowlerblog.com](https://therumhowlerblog.com/rum-reviews/)
- [whiskyscores.com](https://whiskyscores.com)
