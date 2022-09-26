import os
import sys
import boto3
import time
import json
from execution_modules import execute_cofiguration, get_instance_id, get_instance_details


def replace_all(file, dic):
    with open(file) as f:
        file_data = f.read()

    for i, j in dic.items():
        file_data = file_data.replace(i, j)
    return file_data

def main():

    start_time = time.time()

    chefautomate_instanceId, chefserver_instanceId = get_instance_id()

    server_pubIP, server_pubfqdn = get_instance_details(chefserver_instanceId)
    automate_pubIP, automate_pubfqdn = get_instance_details(chefautomate_instanceId)

    tag_replace_dict = {
        "@@@@automate_fqdn@@@@": automate_pubfqdn,
        "@@@@automate_ip@@@@": automate_pubIP,
        "@@@@server_fqdn@@@@": server_pubfqdn,
        "@@@@server_ip": automate_pubIP
    }

    chef_server_config = replace_all('configure_chef_server.sh', tag_replace_dict)
    chef_automate_config = replace_all('configure_chef_automate.sh', tag_replace_dict)

    print(chef_server_config)

    execute_cofiguration(script=chef_server_config, host=server_pubIP, username='ec2-user', pvt_key="/Users/anksoni/Documents/Docs/SecurityPass/AWSKeys/Ankit.pem")

    execute_cofiguration(script=chef_automate_config, host=automate_pubIP, username='ec2-user', pvt_key="/Users/anksoni/Documents/Docs/SecurityPass/AWSKeys/Ankit.pem")

    print("--- %s seconds ---" % (time.time() - start_time))

main()