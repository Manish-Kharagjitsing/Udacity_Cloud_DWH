import configparser
import psycopg2


"""
Test Connections
"""
def aws_connect():
    pass


"""
Test 
"""


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    try:
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        cur = conn.cursor()
    except Exception as e:
        print(e)
        print("Connection Not Established")
    pass



if __name__=="__main__":
    main()