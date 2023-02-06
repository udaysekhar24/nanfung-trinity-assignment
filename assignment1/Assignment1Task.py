import os
import sys
import boto3
import logging
import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
import calendar
from botocore.exceptions import ClientError

RUN_DATE = datetime.today().strftime('%Y-%m-%d')
# Logging setup
logger = logging.getLogger(__name__)
logs_path = 'logs'
log_file_path = "{dir}/{filename}_{date}.log".format(date=RUN_DATE,
                                                     filename=os.path.splitext(os.path.basename(__file__))[0],
                                                     dir=logs_path)
if not os.path.exists(logs_path):
    os.makedirs(logs_path)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=log_file_path, filemode='w')

# Config setup
load_dotenv()
ACCESS_KEY = os.environ.get('aws_access_key')
SECRET_KEY = os.environ.get('aws_secret_key')
BUCKET_NAME = os.environ.get('s3_bucket_name')
TARGET_DIR = "processed/jobposts"
MAX_FILE_COUNT = 3
DEFAULT_FILE_FORMAT = 'csv'
DEFAULT_TARGET = 'dev'


class JobPost(object):

    def __init__(self):
        self.job_title = ''
        self.company_name = ''
        self.company_rating = ''
        self.salary = ''
        self.timestamp_ms = calendar.timegm(datetime.utcnow().utctimetuple())


class Assignment1Task(object):

    max_file_count = MAX_FILE_COUNT
    env = DEFAULT_TARGET
    file_format = DEFAULT_FILE_FORMAT

    def setup(self):
        # Setup starts
        arg_dict = dict()
        if len(sys.argv) > 2:
            for arg in sys.argv:
                arg_dict[arg.split('=')[0]] = arg.split("=")[1]
            if arg_dict.get("env"):
                env = arg_dict["env"]
                if env == "prod":
                    self.max_file_count = int('inf')
            if arg_dict.get("format"):
                self.file_format = arg_dict["format"]
        logger.info("Running for target: " + str(self.env))
        logger.info("File format: " + str(self.file_format))
        # Setup ends

    @staticmethod
    def connect_to_aws_s3(access_key, secret_key):
        aws_session = boto3.Session(aws_access_key_id=access_key,
                                    aws_secret_access_key=secret_key)
        s3_client = aws_session.client('s3')
        s3_resource = aws_session.resource('s3')
        return s3_client, s3_resource

    @staticmethod
    def read_from_s3(file_key, s3_client):
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
        return response['Body']

    @staticmethod
    def parse_html(stream):
        try:
            soup = BeautifulSoup(stream, features="html.parser")
            job_posts_lst = list()
            for table in soup.find_all('table', class_='jobCard_mainContent'):
                all_spans = table.find_all('span')
                new_job_post = JobPost()
                for span in all_spans:
                    # parse Job Title
                    if span.get('title'):
                        new_job_post.job_title = span.get('title')
                    # parse Company Name
                    if span.get('class') and 'companyName' in span.get('class'):
                        new_job_post.company_name = span.get_text()
                    # parse Rating Number
                    if span.get('class') and 'ratingNumber' in span.get('class'):
                        new_job_post.company_rating = span.get_text()
                    # parse Salary
                    if span.get('class') and 'salary-snippet' in span.get('class'):
                        new_job_post.salary = span.get_text()
                job_posts_lst.append(new_job_post.__dict__)
            return job_posts_lst
        except Exception as e:
            raise

    @staticmethod
    # Currently this supports 2 file formats csv and parquet
    def write_to_s3(data_df, path, file_format='csv'):
        if file_format == 'csv':
            data_df.to_csv(path, index=None)
        elif file_format == 'parquet':
            data_df.to_parquet(path, index=None)
        else:
            logger.warning("***********Unsupported file format: %s", file_format)
            return False
        return True

    def run(self):
        logger.info("^^^^~~~~~~^^^^^ Here are the dragons ^^^^~~~~~~^^^^^")
        self.setup()
        s3_client, s3_resource = self.connect_to_aws_s3(access_key=ACCESS_KEY,
                                                        secret_key=SECRET_KEY)
        s3_bucket = s3_resource.Bucket(BUCKET_NAME)

        object_summary_iterator = s3_bucket.objects.filter()
        logger.info("Found: " + str(object_summary_iterator))
        file_counter = 1
        for object_summary in object_summary_iterator:
            try:
                file_key = object_summary.key
                logger.info("Processing file: " + str(file_key))
                # Get html body from s3
                response_stream = self.read_from_s3(file_key, s3_client)
                html_body = response_stream.read()
                # Parse html to a list of type JobPost
                job_posts_lst = self.parse_html(stream=html_body)

                ###
                # Convert lst into a dataframe.
                # Used DF because it will take care of None which coping to CSV and compatible with other data formats.
                # If the size of records in input files grows this can be a bottleneck. But, for now it is managable.
                ###
                job_posts_df = pd.DataFrame(job_posts_lst)

                # Adding source file name for data lineage
                job_posts_df['source'] = file_key

                # Push to s3 bucket
                # Todo: Set up s3 bucket to store processed data.
                # Currently, files are stored in local machine due to write permission denied to s3 bucket provided
                # target_path = 's3://' + BUCKET_NAME + '/processed/' + str(file_counter) + '.' + OUT_FILE_FORMAT
                # self.write_to_s3(job_posts_df, target_path, file_format=OUT_FILE_FORMAT)

                target_path = TARGET_DIR + '/' + RUN_DATE
                file_name = target_path + '/' + str(file_counter) + '.' + self.file_format
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                job_posts_df.to_csv(file_name, index=None)
                file_counter = file_counter + 1
                if file_counter > self.max_file_count:
                    exit(0)
            except ClientError as e:
                logger.warning("~~~~~~~~~~~~~~~~ Error for html query %s: %s", object_summary.key, e.response)
                continue


if __name__ == "__main__":
    a1t = Assignment1Task()
    a1t.run()
