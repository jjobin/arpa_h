# arpa-h
For web scraping teaming partners table on ARPA-H programs pages.

ARPA-H has several programs. (https://arpa-h.gov/research-and-funding/programs)
Each program has a webpage which has a table of teaming partners.
However, this table is a bit unwieldly to read in a web browser due to horizontal/vertical scrolling.

The get_team_table.py script retrieves that table from the webpage and parses the data into a csv file.
The csv can then be read using Excel or pandas if you want to do further processing.

