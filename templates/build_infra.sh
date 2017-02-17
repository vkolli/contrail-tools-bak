source /etc/contrail/openstackrc 

echo $1 >> /root/$1/info.txt
a="$(openstack project create $1 -f json > /root/$1/uuid.json)"
openstack_project_uuid=$(python -c 'import json; fd=json.loads(open("/root/'$1'/uuid.json").read()); print fd["id"]')
dashed_project_uuid=$(python -c 'import uuid; fd=uuid.UUID("'${openstack_project_uuid}'"); print fd')
echo $dashed_project_uuid
sleep 5

sed -i 's/project_uuid_val/'${dashed_project_uuid}'/' /root/$1/input.json
echo "/root/$1/input.json  --- Changed"

python /root/$1/inp_to_yaml.py /root/$1/input.json create_network_yaml > /root/$1/final_network.yaml
python /root/$1/inp_to_yaml.py /root/$1/input.json create_server_yaml > /root/$1/final_server.yaml
echo " The Servere and Network YAML files are now created at location '/root/$1'"

project_uuid=$(python -c 'import json; fd=json.loads(open("/root/'$1'/input.json").read()); print fd["inp_params"]["params"]["project_uuid"]')
network_stack='test_network_final'
final_network_stack_name=$network_stack$project_uuid
echo $final_network_stack_name
echo $final_network_stack_name >> /root/$1/info.txt
server_stack_name='test_server_final'
final_server_stack_name=$server_stack_name$project_uuid
echo $final_server_stack_name
echo $final_server_stack_name >> /root/$1/info.txt

heat stack-create -f /root/$1/final_network.yaml $final_network_stack_name
echo " Network Stack is being created ... Waiting for 30 seconds"
sleep 30
heat stack-create -f /root/$1/final_server.yaml $final_server_stack_name
echo " Server Stack is being created ... Waiting for 150 seconds"
sleep 150
echo " Final List of all Heat Stacks "
heat stack-list 
python /root/$1/inp_to_yaml.py /root/$1/input.json create_cluster_json > /root/$1/cluster.json
python /root/$1/inp_to_yaml.py /root/$1/input.json create_server_json > /root/$1/server.json
python /root/$1/inp_to_yaml.py /root/$1/input.json get_sm_ip > /root/$1/server-manager-file
python /root/$1/inp_to_yaml.py /root/$1/input.json get_config_node_ip > /root/$1/config-node-ip
python /root/$1/inp_to_yaml.py /root/$1/input.json create_testbedpy_file > /root/$1/testbed.py
echo " -----   DONE  -----"
