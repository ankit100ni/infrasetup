#!/bin/bash
# This script will update the the Chef Server after the regular AWS machine shutdown

echo "Configuring the hostname with new public DNS"
sudo hostnamectl set-hostname @@@@server_fqdn@@@@
if [ $? -eq 0 ]; then
    echo "hostname is set on Chef Automate server successfully"
else
    echo "ERROR : Failed to set hostname on Chef Automate, please set it manually"
fi

echo "Configuring the Chef Automate url on path /etc/opscode/chef-server.rb"

sudo tee /etc/opscode/chef-server.rb > /dev/null <<EOT
data_collector['root_url'] = 'https://@@@@automate_fqdn@@@@/data-collector/v0/'
# Add for Chef Infra Client run forwarding
data_collector['proxy'] = true
# Add for compliance scanning
profiles['root_url'] = 'https://@@@@automate_fqdn@@@@'
# Save and close the file
EOT

echo "Reconfiguring the chef server configuration"
sudo chef-server-ctl reconfigure