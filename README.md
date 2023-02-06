# nanfung-trinity-assignment

### **Questions**
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

### **Requirement**
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

### **Execution steps**

Prerequisites
* Python 3
* pip

Note: replace text with `<>` to actual values
1. Download and unzip the assignment.zip folder 
2. Run `cd <path-to-assignment-folder>`
3. Create a virtual environment using cmd
    `py -v venv assignment_venv`
4. Load virtual environment
    `assignment_venv\Scripts\activate`
5. Run `py -m pip install --upgrade pip`
6. Run `pip install -r requirements.txt`
7. Create .env file in root dir of this project  
8. In .env paste below lines and save

   `aws_access_key = '<aws-access-key>'`

   `aws_secret_key = '<aws-secret-key>'`

   `s3_bucket_name = 'ext-candidate-data'`
9. Run `py -m pytest`
10. Run `deactivate`
11. Output files are stored in `processed` folder

### **Assignment 1 Design** <br>
* Assumptions:
    * For dev/test, I have restricted to `3` files.
    * I did not have write permissions for s3 bucket provided hence, storing processed file to disk. But, code to upload to s3 is available but commented
* Output dir path: `process/jobposts/<date>`
* Output formats supported: `csv` or `parquet`
* _For PRODUCTION:_ `py assignment.Assignement1Task env=PROD format=csv`

![assignment1_design.JPG](docs%2Fassignment1_design.JPG)

### **Assignment 2 Design** <br>
* Assumptions:
    * I did not have write permissions for s3 bucket provided hence, storing processed file to disk. But, code to upload to s3 is available but commented
* Output dir path: `process/products/<date>`
* Output formats supported: `csv` or `parquet`
* For daily cadence schedule below command. As processed files are stored by date there is no problem of overwrite. 
* _For PRODUCTION:_ `py assignment.Assignement2Task env=PROD format=csv`

![assignment2_design.JPG](docs%2Fassignment2_design.JPG)

**Assignment 3: Minimum spanning tree**

There are many ways to solve for minimum spanning tree
1. Prim's Algorith
2. Kruskal's Algorithm
3. Fibonacci Heaps

For this assignment I choose to implement using Prim's Algorithm

#### **Prim's algorithm logic:**

1. Choose any vertex as source
2. Find the minimum weight edge for traversal to next vertex such that there are no cycles and add it to tree.
3. Keep repeating this process until we traverse all the vertices in the graph.

_Required input:_
* num_vertices: Number of vertices in the input graph 
* graph: This is an adjacency matrix to depict the graph. Each cell represents edge and its traversal weight.


Output:
* mst: minimum spanning tree as adjacency matrix
* traversl_cost: cost of traversing all the vertices

### **Assignment 4: LRU Cache**


LRU Cache can be implemented using a dict(cache) and DoublyLinkedList(DLL)
methods:

#### **Logic**

get(key):

       Search key in cache
           Yes: Set key as HEAD in DLL and return contents
           No: return None
   
put(key, content):

       Search key in cache
           Yes: Update content and set node to HEAD
           No:
               Check if size of cache is not maximum
                   Yes: Add node to cache and set it to HEAD
                   No: Remove TAIL node and Add node to cache and set it to HEAD

**Testing summary results**

![assignment_testcase_summary.JPG](docs%2Fassignment_testcase_summary.JPG)