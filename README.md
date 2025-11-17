Hackathon Rules for Building the script 
Your task is to build a web scraper that extracts all Development Application (DA) details for the date range 1st September 2025 – 30th September 2025 from the Shoalhaven City Council's DA Tracking portal.

The scraper must follow the precise step-by-step instructions below, including handling navigation, pagination, data cleaning, and final storage.

🧭 Technical Specification: Step-by-Step Instructions

Step 1: Navigate and Agree
URL: https://www3.shoalhaven.nsw.gov.au/masterviewUI/modules/ApplicationMaster/Default.aspx

Action: Programmatically click “Agree” on the disclaimer page to proceed.

Step 2: Go to DA Tracking
Action: After agreeing, click on the “DA Tracking” tab located in the top navigation bar.

Step 3: Select Advanced Search
Action: Click on the “Advanced Search” tab to reveal the date range filters.The Image is given below for refrence

Step 4: Set Date Range and Search
Action: Set the date range in the provided input fields:

From: 01/09/2025

To: 30/09/2025

Then, click the Search button.


Step 5: Load and Scrape All Results
Action: Click the “Show” button to display the results.

Your scraper must handle pagination to load and process all available records for the specified date range (approximately 215 results).

Scrape all records sequentially, ensuring no duplicates are collected.


Step 6: Apply Data Cleaning Rules
Before storing the data, implement the following cleaning logic. This is a critical step to test attention to detail.

In the Fees section of each record:

If the scraped text is exactly No fees recorded against this application.

Then the value stored in the Fees column must be “Not required”.

In the Contact Council section of each record:

If the scraped text is exactly Application Is Not on exhibition, please call Council on 1300 293 111 if you require assistance.

Then the value stored in the Contact Council column must be “Not required”.

The Image is given below for refrence
(Note: All other fields and values should be stored as-is without modification.)

Step 7: Store Data in CSV Format
Action: Store all extracted and cleaned data into a single CSV file.

The file must use the following headers exactly as written:

Step 7: Final CSV should Look Like these headers
DA_Number
Detail_URL
Description
Submitted_Date
Decision
Categories
Property_Address
Applicant
Progress
Fees
Documents
Contact_Council
The Image is given below for refrence


Additional Points:
Content: Each column should contain the raw content (text)found under its corresponding section on the website, except for the fields modified in Step 6.

Completeness: The final CSV file should contain all records from all pages.

- The script should be submitted in 7 hours from 1:00 PM to 8:00 PM on 15-11-2025

_________________________________________________________________________________________________________________________________________________________

