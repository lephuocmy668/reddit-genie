from pyspark import SparkContext, SQLContext
import sys
import ast
from nltk import word_tokenize
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config/')
from constants import FILTER_SET
from cassandra.cluster import Cluster
from boto.s3.connection import S3Connection
from os import environ
import json
import logging
from elasticsearch import Elasticsearch

SPARK_ADDRESS = sys.argv[1]
APP_NAME = "Reddit JSON Parser App"

def put_to_elasticsearch(partition):
    hosts=["ec2-52-35-132-98.us-west-2.compute.amazonaws.com", "ec2-52-34-176-185.us-west-2.compute.amazonaws.com", "ec2-52-89-115-101.us-west-2.compute.amazonaws.com", "ec2-52-88-254-51.us-west-2.compute.amazonaws.com", "ec2-52-88-247-22.us-west-2.compute.amazonaws.com", "ec2-52-89-166-197.us-west-2.compute.amazonaws.com"]
    logs_file_path = os.path.dirname(os.path.abspath(__file__)) + '/logs/'
    if not os.path.exists(logs_file_path):
        os.makedirs(logs_file_path)
    logging.basicConfig(filename=logs_file_path + 'reddit-spark-elasticsearch-bulk.log',level=logging.DEBUG)
    es = Elasticsearch(
        hosts,
        port=9201,
        sniff_on_start=True,    # sniff before doing anything
        sniff_on_connection_fail=True,    # refresh nodes after a node fails to respond
        sniffer_timeout=60, # and also every 60 seconds
        timeout=30
    )
    i = 0
    if partition:
        json_string = ''
        for item in partition:
            json_string += item
            json_string += '\n'
#           preparedStmt = session.prepare("INSERT INTO {0} ({1}, {2}, {3}) VALUES (?, ?, ?)".format(GRAPH_NAME, PRIMARY_KEY, PARTITION_KEY, DICTIONARY))
 #          boundStmt = preparedStmt.bind([item[0], item[1][0], item[1][1]]) #username then subreddit
  #         session.execute(boundStmt)
#        print json_string
        es.bulk(body=json_string)
    #except Exception as e:
     #   logging.error("could not write to elasticsearch with error: {0}".format(str(e)))
    
def elastic_search_mapper(df):
    final_string = ""
    action_json = {'index': {'_index': 'reddit_filtered', '_type': 'comment', '_id': df.id}}  
    final_string += json.dumps(action_json)
    final_string +='\n'
    es_comment_json = {}
    es_comment_json['author'] = df.author
    es_comment_json['subreddit'] = df.subreddit
    es_comment_json['score'] = df.score
    es_comment_json['created_utc'] = long(df.created_utc)
    es_comment_json['filtered_body'] = get_filtered_string(df.body)
    final_string += json.dumps(es_comment_json)
    return final_string

def get_filtered_string(original_string):
    tokenized_list = word_tokenize(original_string.lower())
    filtered_tokenized_list = [word for word in tokenized_list if word not in FILTER_SET]
    return ' '.join(filtered_tokenized_list)
    
sc = SparkContext(SPARK_ADDRESS, "Reddit JSON Parser App")
sql_context = SQLContext(sc)

conn = S3Connection(environ['AWS_ACCESS_KEY_ID'], environ['AWS_SECRET_ACCESS_KEY'])
reddit_bucket = conn.get_bucket('reddit-comments')
my_bucket = conn.get_bucket('mark-wang-test')
for key in reddit_bucket.list():
    if '-' not in key.name.encode('utf-8'):
        continue
    logFile = 's3n://reddit-comments/' + key.name.encode('utf-8')
    year = logFile.split('-')[1][-4:]
    if year != '2007':
        continue
    month = logFile.split('-')[2]
    year_month = '{0}_{1}'.format(year, month)
    df = sql_context.read.json(logFile)
    filtered_df = df.filter(df.author != '[deleted]')
    final_rdd = filtered_df.map(lambda line: elastic_search_mapper(line))
    final_rdd.foreachPartition(put_to_elasticsearch)

#    outputDirectory = 's3n://mark-wang-test/reddit-es-comments-json/{0}/'.format(year_month)
    # delete files if it already exists.
 #   for my_key in my_bucket.list(prefix='reddit-es-comments-json/{0}'.format(year_month)):
 #       my_key.delete()
#    final_string.saveAsTextFile(outputDirectory)

sc.stop()
