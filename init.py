import os
import sys
import boto3
import time
import json
from execution_modules import execute_cofiguration, get_instance_id, get_instance_details, get_pvt_key


def replace_all(file, dic):
    with open(file) as f:
        file_data = f.read()

    for i, j in dic.items():
        file_data = file_data.replace(i, j)
    return file_data

def main():

    start_time = time.time()

    chefautomate_instanceId, chefserver_instanceId = get_instance_id()
    boto_client = boto3.client('ec2')
    boto_client.start_instances(InstanceIds=[chefautomate_instanceId,chefserver_instanceId,])

    pvt_key = get_pvt_key()
    
    clock_count = 0
    
    while clock_count < 10:
        server_status = boto_client.describe_instance_status(InstanceIds=[chefserver_instanceId,])
        automate_status = boto_client.describe_instance_status(InstanceIds=[chefautomate_instanceId,])

        if server_status['InstanceStatuses'] and automate_status['InstanceStatuses']:
            print("Servers are up, waiting for 30 seconds before starting configuration")
            time.sleep(30)
            break
        
        print(f"{clock_count} attempt in 10 seconds")
        time.sleep(10)
        clock_count = clock_count+1


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

    execute_cofiguration(script=chef_server_config, host=server_pubIP, username='ec2-user', pvt_key=pvt_key)

    execute_cofiguration(script=chef_automate_config, host=automate_pubIP, username='ec2-user', pvt_key=pvt_key)

    print("--- %s seconds ---" % (time.time() - start_time))

main()