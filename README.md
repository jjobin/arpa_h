# arpa-h

Scripts to work with ARPA-H data.

## get_team_table.py

For web scraping teaming partners table on ARPA-H programs pages.

ARPA-H has several programs. (https://arpa-h.gov/research-and-funding/programs)
Each program has a webpage which has a table of teaming partners.
However, this table is a bit unwieldly to read in a web browser due to horizontal/vertical scrolling.

The get_team_table.py script retrieves that table from the webpage and parses the data into a csv file.
The csv can then be read using Excel or pandas if you want to do further processing.

## fundingmap.py

ARPA-H does a great job of maintaining a list of awarded programs, all on a single page:
https://arpa-h.gov/research-and-funding/mission-office-iso/awardees

The fundingmap.py retrieves this data, converts city names to latitude/longitude values, creates a map with this information.
The size of the circles is proportional to the funding amount: bigger circles = larger funded amounts.

