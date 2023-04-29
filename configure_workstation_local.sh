echo "Configuring workstation on local"

echo "Updating the credentials file"

tee cat ~/.chef/credentials > /dev/null <<EOT
[default]
client_name     = 'chefadmin'
client_key      = '/Users/anksoni/.chef/chefadmin.pem'
chef_server_url = 'https://@@@@server_fqdn@@@@/organizations/qa'
EOT

echo "Fetching updated certificates"
knife ssl fetch

knife ssl check
if [ $? -eq 0 ]; then
    echo "Fetched certificates successfully"
else
    echo "ERROR : Failed to set fetch certificates"
fi