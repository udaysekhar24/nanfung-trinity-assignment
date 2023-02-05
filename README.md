# nanfung-trinity-assignment

Questions
1. Build an ETL pipeline that reads the raw data in S3, extract the key data points, and
save the final data (You can save it anywhere, can be your own S3 bucket). The data
which is provided to you is the raw html extracted from a job posting website. The
raw html contains key information such as job title and salary. Your task is to extract
that information and save it into a more structural format (column-based data). You
are highly encouraged to make use of AWS EMR for big data processing as the data
size is large. Please prepare design diagrams, code base, and some samples for the
transformed data for discussion. The final dataset must include the following 3
columns but not limited to: Job title, Salary, timestamp the data is collected (the folder
name which contains the raw data has been conveniently named to indicate the
collected time). The file name indicates the html query used to retrieve the raw html.
e.g. jobs?q=construction%20worker&sort=date&limit=50&fromage=1&start=0
indicates we get the html by firing a query for construction worker.

2. Build a web scraper that scrapes https://www.michaelkors.com/ on a daily cadence.
Please focus only on extracting the price/item data for the women handbag category.
Handling of page pagination is great to have but not a must. Ideally, you can cache the
entire page and have separate programs to extract the item price/product info into a
more structural format. The scraper is expected to run on a regular cadence so please
incorporate that into your design. Please prepare design diagrams that illustrate key
components of your systems, code base, and some collected data samples for
discussion. Collected data must include but not limited to the following 3 columns:
Product name, Price, timestamp when the data is collected.

3. Find the minimum spanning tree of a connected, undirected graph with weighted
edges. Please submit the code with sufficient comments.

4. Implement a Least Recently Used (LRU) cache. LRU is a type of data structure which
evicts elements from the cache to make room for new elements when the cache is
full. It discards the least recently used items first. Please submit the code with
sufficient comments.

Requirement
1. Python is strongly preferred for implementation.
2. Please include documentation that will allow us to set up the environment with the
required dependencies to run the code successfully on our side. Your code is expected
to be fully functional.
3. For question #1, #2, you are free to use any open-source library. You are highly
encouraged to make use of AWS services such as EMR and S3 to complete the task.
4. For question #3, #4, You can present your solution in a Jupyter Notebook or python
scripts. Please include sufficient comments in your code and test cases to handle edge
cases.
5. There will be a debrief session after the exercise.
