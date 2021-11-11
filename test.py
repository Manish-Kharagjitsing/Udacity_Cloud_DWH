import configparser
import psycopg2


"""
The purpose of this script is to first check whether a connection
with AWS Redshift can be established. 

If so, the properties of the Redshift Cluster is shown. 
"""




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
    aws_connect()
    myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    prettyRedshiftProps(myClusterProps)
    pass



if __name__=="__main__":
    main()