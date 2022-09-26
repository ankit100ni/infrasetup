# Configuration of Chef Infra setup
The script is created to automate the process for reconfiguring Chef Automate and Chef Server with updated IP and FQDN after the daily shut down of servers

## Solution preface
- Start the ec2 instances with the help of instnace Ids mentioned in config.json
- Configure Chef Server
    - Set the new hostname from AWS console
    - Update integration with Chef Automate server by adding configuration on path /etc/opscode/chef-server.rb
- Configure Chef Automate Server
    - Set the new hostname from AWS console
    - Update the config.toml file, present on home directory, in case config.toml is kept as some custom location, appropriate changes needs to be made in script configure_chef_automate.sh on line 16.
    - Patch of configuration.
    - Restart the services.

## Constraints
- As of now, script is created only for Amazon linux, in case any other platform is used, appropriate chagnes needs to made while calling the execute_cofiguration function in init.py line 58 and 60.
- in case config.toml is kept as some custom location, appropriate changes needs to be made in script configure_chef_automate.sh on line 16.

## ** Please feel free to add any issues in issues tab **