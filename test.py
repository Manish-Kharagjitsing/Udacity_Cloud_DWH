import configparser
from boto3 import client
import boto3
import psycopg2
import pandas as pd


"""
The purpose of this script is to first check whether a connection
with AWS Redshift can be established. 

If so, the properties of the Redshift Cluster are shown. 
"""
#######################################################################################
# GET ALL REQUIRED  VARIABLES. 
# THE VARIABLES CONSISTS OF 
# 
#######################################################################################

config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

KEY= config.get('AWS','KEY')
SECRET= config.get('AWS','SECRET')
DWH_CLUSTER_TYPE= config.get("DWH","DWH_CLUSTER_TYPE")
DWH_NUM_NODES= config.get("DWH","DWH_NUM_NODES")
DWH_NODE_TYPE= config.get("DWH","DWH_NODE_TYPE")

DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
DWH_DB = config.get("CLUSTER","DB_NAME")
DWH_DB_USER = config.get("CLUSTER","DB_USER")
DWH_DB_PASSWORD = config.get("CLUSTER","DB_PASSWORD")
DWH_PORT = config.get("CLUSTER","DB_PORT")
DWH_IAM_ROLE_NAME = config.get("DWH", "DWH_IAM_ROLE_NAME")


#######################################################################################
# Create AWS Clients 
# 
#######################################################################################


def clients():
    ec2 = boto3.resource('ec2',
                        region_name="us-west-2",
                        aws_access_key_id=KEY,
                        aws_secret_access_key=SECRET
                    )

    s3 = boto3.resource('s3',
                       region_name="us-west-2",
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET
                   )

    iam = boto3.client('iam',
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET,
                       region_name='us-west-2'
                  )

    redshift = boto3.client('redshift',
                       region_name="us-west-2",
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET
                  )

    return redshift,iam




#######################################################################
# Redshift Cluster properties 
#######################################################################

def prettyRedshiftProps(props):
    """
    This function checks the properties of the cluster and
    returns is in a dataframe. 
    """
    pd.set_option('display.max_colwidth', -1)
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])



def aws_connect():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    try:
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        cur = conn.cursor()
    except Exception as e:
        print(e)
        print("Connection Not Established")


def main():
    redshift, iam = clients()
    # aws_connect()
    myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    print(prettyRedshiftProps(myClusterProps))
    pass



if __name__=="__main__":
    main()