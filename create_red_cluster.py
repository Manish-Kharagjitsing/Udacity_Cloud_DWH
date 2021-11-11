import boto3
import configparser
import json


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
DWH_DB = config.get("DB","DB_NAME")
DWH_DB_USER = config.get("DB","DB_USER")
DWH_DB_PASSWORD = config.get("DB","DB_PASSWORD")
DWH_PORT = config.get("DB","DB_PORT")
DWH_IAM_ROLE_NAME = config.get("DWH", "DWH_IAM_ROLE_NAME")

#######################################################################################
# CREATE THE CLIENTS SO THAT WE AUTOMATE OUR INFRASTRUCTURE
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


#######################################################################################
# CREATE THE IAM ROLE THAT ALLOWS REDSHIFT TO CALL AWS SERVICES 
# 
#######################################################################################

def create_iam_role_arn(iam):
    try:
        print("1.1 Creating a new IAM Role") 
        dwhRole = iam.create_role(
            Path='/',
            RoleName=DWH_IAM_ROLE_NAME,
            Description = "Allows Redshift clusters to call AWS services on your behalf.",
            AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                'Effect': 'Allow',
                'Principal': {'Service': 'redshift.amazonaws.com'}}],
                'Version': '2012-10-17'})
        )
    except Exception as e:
        print(e)

    print("1.2 Attaching Policy")

    iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME,PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")['ResponseMetadata']['HTTPStatusCode']
    
    print("1.3 Get the IAM role ARN")
    roleArn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']

    return roleArn

#######################################################################################
# CREATE THE REDSHIFT CLUSTER 
# 
#######################################################################################



def create_red_clust(redshift, iam_role):
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
            IamRoles=[iam_role]  
        )
        print("Creating cluster")
    except Exception as e:
        print(e)

    pass


#######################################################################################
# CALL THE MAIN PROGRAM. 
# 
#######################################################################################

def main():
    redshift_client,iam = clients()
    iam_role = create_iam_role_arn(iam)
    create_red_clust(redshift_client, iam_role)
    pass


if __name__=="__main__":
    main()