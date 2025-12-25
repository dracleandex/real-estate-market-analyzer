\# Real Estate Market Analyzer <PropTech Commander> 🏠



A custom data pipeline and dashboard I built to track housing prices, spot market anomalies, and find undervalued properties automatically.



\## 💡 Why I Built This

I realized that browsing sites like Zillow or Redfin manually is inefficient. You can't easily compare historical trends, and by the time you spot a "good deal," it's often too late.



I wanted a tool that could:

1\.  \*\*Automate the busy work:\*\* Scrape listings while I sleep.

2\.  \*\*Clean the data:\*\* Fix messy formats and remove duplicates automatically.

3\.  \*\*Do the math for me:\*\* Compare valid listings against the city average to flag actual deals.



\## ⚙️ How It Works (The Workflow)

This isn't just a scraper; it's a full data application. Here is the flow:



1\.  \*\*Collection:\*\* I wrote custom scrapers (using `BeautifulSoup` and `requests`) that can target specific sites or search globally. I built a `ScraperFactory` to make it easy to add new websites later without breaking existing code.

2\.  \*\*Cleaning \& Storage:\*\* Raw web data is notoriously dirty. I use \*\*Pandas\*\* to clean currency symbols, fix address formatting, and remove duplicates before saving everything to a SQL database.

3\.  \*\*Analysis:\*\* The system calculates the "Market Health" of each city. It looks at price volatility (standard deviation) to see if a market is stable or risky.

4\.  \*\*Reporting:\*\* I built an export engine that converts the clean data into usable formats for different needs.



\## 🛠️ Tech Stack

\* \*\*Python 3.10+\*\* (Core logic)

\* \*\*Pandas:\*\* For data manipulation and statistical analysis.

\* \*\*Flask:\*\* For the web interface and API.

\* \*\*BeautifulSoup4:\*\* For parsing HTML and web scraping.

\* \*\*SQLite / SQLAlchemy:\*\* For persistent data storage.

\* \*\*FPDF:\*\* For generating multi-page PDF reports.



\## 🚀 Key Features



\### 1. Robust Data Exporting

I designed the system to be flexible with how data is delivered. It supports:

\* \*\*CSV:\*\* Clean, structured files ready for Excel or further analysis.

\* \*\*JSON:\*\* Formatted output for API integration or NoSQL storage.

\* \*\*PDF:\*\* Professional, auto-paginated reports (handling unlimited rows) for sharing summaries with stakeholders.



\### 2. Deal Hunter Algorithm

Automatically flags properties that are \*\*10% (or more) below\*\* the local market average, helping users find value quickly.



\### 3. Market Health Radar

Visualizes which cities have the most volatile pricing using standard deviation metrics, displayed via interactive charts.



\## 💻 How to Run It



\*\*1. Install Dependencies\*\*

```bash

pip install -r requirements.txt

2\. Collect Data Run the scraper from the command line (CLI) to fetch the latest listings.



Bash



python src/api/cli.py scrape --pages 2

3\. Analyze \& View Dashboard Start the web server to see the analytics and download reports.



Bash



python src/web/app.py

Then open http://127.0.0.1:5000 in your browser.



🔍 Project Status

This is currently a functional MVP.



Current Focus: Refining the scraping logic to handle more complex dynamic HTML.



Next Steps: I plan to migrate the database to PostgreSQL for better concurrency and add Celery for background task scheduling.



Created by Olayemi Daniel

