#!/bin/bash
# This script will update the the Chef Automate server after the regular AWS machine shutdown

echo "Configuring the hostname with new public DNS"
sudo hostnamectl set-hostname @@@@automate_fqdn@@@@


if [ $? -eq 0 ]; then
    echo "hostname is set on Chef Automate server successfully"
else
    echo "ERROR : Failed to set hostname on Chef Automate, please set it manually"
fi

sudo sed -i 's/ec2.*com/@@@@automate_fqdn@@@@/g' config.toml

sudo chef-automate config patch config.toml
if [ $? -eq 0 ]; then
    echo "Chef Automate server is updated"
else
    echo "ERROR : Failed to update Chef Automate server"
fi
echo "Restarting the Automate server services"
sudo chef-automate restart-services

