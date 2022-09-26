from pydoc import cli
import paramiko
import boto3
import json



def execute_cofiguration(script, host, username, pvt_key):
    key  = paramiko.RSAKey.from_private_key_file(pvt_key)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"Connecting to the host {host}")
    try:
        client.connect(hostname=host, username=username, pkey=key)
        print('Host Connected Succefully')
    except Exception as e:
        print("###########################  Exception Occured ###########################")
        print(f"There is an error while connecting the host {host} \n {e}")

    stdin, stdout, stderr = client.exec_command(script)
    print("############################ Execution Output ###########################")
    print(stdout.read())

    if stderr:
        print("########################## Error in Exectuion of script on host #######################################")
        print(stderr.read())
    client.close()


def get_instance_details (instanceID):
    ec2 = boto3.client("ec2")
    res = ec2.describe_instances(InstanceIds=[instanceID,])

    pub_IP = res["Reservations"][0]["Instances"][0]["PublicIpAddress"]
    pub_fqdn = res["Reservations"][0]["Instances"][0]["PublicDnsName"]

    return pub_IP, pub_fqdn


def get_instance_id():
    with open('config.json') as f:
        instance_details = json.load(f)
    return instance_details['InstanceId']['chef_automate'], instance_details['InstanceId']['chef_server']
