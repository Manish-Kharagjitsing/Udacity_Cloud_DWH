import boto3
import configparser


config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

KEY= config.get('AWS','KEY')
SECRET= config.get('AWS','SECRET')
DWH_CLUSTER_TYPE= config.get("DWH","DWH_CLUSTER_TYPE")
DWH_NUM_NODES= config.get("DWH","DWH_NUM_NODES")
DWH_NODE_TYPE= config.get("DWH","DWH_NODE_TYPE")

DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
DWH_DB = config.get("DB","DB_NAME")
DWH_DB_USER = config.get("DB","DB_USER")
DWH_DB_PASSWORD = config.get("DB","DB_PASSWORD")
DWH_PORT = config.get("DB","DB_PORT")
DWH_IAM_ROLE_NAME = config.get("IAM_ROLE", "ARN")



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

    

def create_red_clust():
    try:
        response = redshift.create_cluster(
            ClusterType=DWH_CLUSTER_TYPE,
            NodeType=DWH_NODE_TYPE,
            NumberOfNodes=int(DWH_NUM_NODES),
            #Identifiers & Credentials
            DBName=DWH_DB,
            ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
            MasterUsername=DWH_DB_USER,
            MasterUserPassword=DWH_DB_PASSWORD,
            #Roles (for s3 access)
            IamRoles=[roleArn]  
        )
    except Exception as e:
        print(e)

    pass


def main():
    clients()
    create_red_clust()
    pass


if __name__=="__main__":
    main()