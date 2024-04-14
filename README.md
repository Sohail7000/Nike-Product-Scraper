
---

# Nike Product Scraper

This Python script is designed to scrape product details from the Nike website, process the data, and store it in a MongoDB database.

## Overview

The script performs the following tasks:

1. Opens a Chrome WebDriver to navigate to the Nike website.
2. Extracts links to individual product pages from the product listing page.
3. Visits each product page to scrape details such as product title, category, price, description, review count, and rating.
4. Stores the scraped data in a pandas DataFrame.
5. Cleans up the data using regular expressions to extract numeric values and convert them to appropriate data types.
6. Connects to a MongoDB database using PyMongo.
7. Inserts the cleaned data into a MongoDB collection.

## Requirements

- Python 3.x
- Selenium
- Pandas
- PyMongo
- Chrome WebDriver

## Usage

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/your_username/nike-product-scraper.git
   ```

2. Create a `config.py` file in the project directory with your MongoDB connection URL:

   ```python
   # config.py

   MONGO_URL = "mongodb+srv://username:password@your-cluster.mongodb.net/your-database"
   ```

   Replace `"mongodb+srv://username:password@your-cluster.mongodb.net/your-database"` with your actual MongoDB connection URL.

3. Install the required Python packages:

   ```
   pip install selenium pandas pymongo
   ```

4. Download the Chrome WebDriver and place it in the same directory as the script.

5. Run the script:

   ```
   python nike_product_scraper.py
   ```

6. Monitor the console for progress updates and any errors.

## Configuration

- Store sensitive information such as the MongoDB connection URL in the `config.py` file and add it to your `.gitignore` to prevent it from being committed to your repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

