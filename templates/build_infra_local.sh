source /etc/contrail/openstackrc 
echo $1 >> /root/heat/final_scripts/new_rev/my_current_working/info.txt
a="$(openstack project create $1 -f json > /root/heat/final_scripts/new_rev/my_current_working/uuid.json)"
openstack_project_uuid=$(python -c 'import json; fd=json.loads(open("/root/heat/final_scripts/new_rev/my_current_working/uuid.json").read()); print fd["id"]')
dashed_project_uuid=$(python -c 'import uuid; fd=uuid.UUID("'${openstack_project_uuid}'"); print fd')
echo $dashed_project_uuid
ubuntu_image_name=$2
sleep 5
cat /root/heat/final_scripts/new_rev/my_current_working/input.json

sed -i 's/project_uuid_val/'${dashed_project_uuid}'/' /root/heat/final_scripts/new_rev/my_current_working/input.json
echo "/root/templates/input.json  --- Changed"

python /root/heat/final_scripts/new_rev/my_current_working/change_testbed_params.py /root/heat/final_scripts/new_rev/my_current_working/input.json $ubuntu_image_name parse_openstack_image_list_command
sleep 5
sed -i 's/image_val/'${ubuntu_image_name}'/' /root/heat/final_scripts/new_rev/my_current_working/input.json
echo "/root/templates/input.json  --- Changed"
echo "\n The Input.json looks something like this now"
cat /root/heat/final_scripts/new_rev/my_current_working/input.json

mkdir /root/$dashed_project_uuid
python /root/heat/final_scripts/new_rev/my_current_working/inp_to_yaml.py /root/heat/final_scripts/new_rev/my_current_working/input.json create_network_yaml > /root/$dashed_project_uuid/final_network.yaml
python /root/heat/final_scripts/new_rev/my_current_working/inp_to_yaml.py /root/heat/final_scripts/new_rev/my_current_working/input.json create_server_yaml > /root/$dashed_project_uuid/final_server.yaml
echo " The Servere and Network YAML files are now created at location '/root/heat/final_scripts/'"

project_uuid=$(python -c 'import json; fd=json.loads(open("/root/heat/final_scripts/new_rev/my_current_working/input.json").read()); print fd["inp_params"]["params"]["project_uuid"]')
network_stack='test_network_final'
final_network_stack_name=$network_stack$project_uuid
echo $final_network_stack_name
echo $final_network_stack_name >> /root/heat/final_scripts/new_rev/my_current_working/info.txt
server_stack_name='test_server_final'
final_server_stack_name=$server_stack_name$project_uuid
echo $final_server_stack_name
echo $final_server_stack_name >> /root/heat/final_scripts/new_rev/my_current_working/info.txt

heat stack-create -f /root/$dashed_project_uuid/final_network.yaml $final_network_stack_name
echo " Network Stack is being created ... Waiting for 10 seconds"
sleep 30
heat stack-create -f /root/$dashed_project_uuid/final_server.yaml $final_server_stack_name
echo " Server Stack is being created ... Waiting for 30 seconds"
sleep 150
echo " Final List of all Heat Stacks "
heat stack-list 
python /root/heat/final_scripts/new_rev/my_current_working/inp_to_yaml.py /root/heat/final_scripts/new_rev/my_current_working/input.json create_cluster_json > /root/$dashed_project_uuid/cluster.json
echo "Cluster.json created "
python /root/heat/final_scripts/new_rev/my_current_working/inp_to_yaml.py /root/heat/final_scripts/new_rev/my_current_working/input.json create_server_json > /root/$dashed_project_uuid/server.json
echo "server.json created "
python /root/heat/final_scripts/new_rev/my_current_working/inp_to_yaml.py /root/heat/final_scripts/new_rev/my_current_working/input.json get_sm_ip > /root/$dashed_project_uuid/server-manager-file
echo "server-manager-ip file created that contains the server-manager ip"
python /root/heat/final_scripts/new_rev/my_current_working/inp_to_yaml.py /root/heat/final_scripts/new_rev/my_current_working/input.json get_config_node_ip > /root/$dashed_project_uuid/config-node-ip
echo "config-node-ip file created that contains the config node ip"
python /root/heat/final_scripts/new_rev/my_current_working/inp_to_yaml.py /root/heat/final_scripts/new_rev/my_current_working/input.json create_testbedpy_file > /root/$dashed_project_uuid/testbed.py
echo "Testbed.py created "
echo " -----   DONE  -----"
