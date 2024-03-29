source /etc/contrail/openstackrc 
echo $1 >> /root/$1/info.txt
a="$(openstack project create $1 -f json > /root/$1/uuid.json)"
openstack_project_uuid=$(python -c 'import json; fd=json.loads(open("/root/'$1'/uuid.json").read()); print fd["id"]')
dashed_project_uuid=$(python -c 'import uuid; fd=uuid.UUID("'${openstack_project_uuid}'"); print fd')
echo $dashed_project_uuid
ubuntu_image_name=$2
sleep 5
echo "The Contents of the input.json file before modification "
cat /root/$1/input.json

sed -i 's/project_uuid_val/'${dashed_project_uuid}'/' /root/$1/input.json
python /root/$1/change_testbed_params.py /root/$1/input.json $ubuntu_image_name parse_openstack_image_list_command
sleep 5
sed -i 's/image_val/'${ubuntu_image_name}'/' /root/$1/input.json
echo "/root/$1/input.json  --- Changed"
echo "The New imput.json :- \n"
cat /root/$1/input.json

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

#Lets Create the Network Stack
heat stack-create -f /root/$1/final_network.yaml $final_network_stack_name
sleep 10
while true
do
python /root/$1/change_testbed_params.py /root/$1/input.json $final_network_stack_name get_stack_status > /root/$1/tmp.txt
chmod 777 /root/$1/tmp.txt
net_res="$(cat /root/$1/tmp.txt)"
if [ "$net_res" == 'success' ] || [ "$net_res" == 'failed' ] || [ "$net_res" == 'inprogress' ];
then
        if [ "$net_res" == 'success' ]
        then
                echo "Network Stack Created Successfully"
                break
        fi
        if [ "$net_res" == 'failed' ]
        then
                echo "Network Stack Creation Failed "
                break
        fi
        if [ "$net_res" == 'inprogress' ]
        then
                echo "Network Stack creation still in progress. Waiting for 20 more seconds"
                heat stack-list | grep $final_network_stack_name
                sleep 20
        fi
else
        echo "Network Stack Creation: get_stack_status function in change_testbed_params.py file did not return any thing"
        break
fi
done

# Now Lets Create The Server Stack 
if [ "$net_res" == 'success' ]
then
	heat stack-create -f /root/$1/final_server.yaml $final_server_stack_name
	sleep 20
        while true
        do
	python /root/$1/change_testbed_params.py /root/$1/input.json $final_server_stack_name get_stack_status > /root/$1/tmp.txt
        chmod 777 /root/$1/tmp.txt
        ser_res="$(cat /root/$1/tmp.txt)"
        if [ "$ser_res" == 'success' ] || [ "$ser_res" == 'failed' ] || [ "$ser_res" == 'inprogress' ];
        then
                if [ "$ser_res" == 'success' ]
                then
                        echo "Server Stack Created Successfully"
                        break
                fi
                if [ "$ser_res" == 'failed' ]
                then
                        echo "Server Stack Creation Failed"
                        break
                fi
                if [ "$ser_res" == 'inprogress' ]
                then
                        echo "Server Stack Still in progress. Waiting for 30 more seconds"
                        heat stack-list | grep $final_server_stack_name
                        sleep 30
                fi
        else
                echo "Server Stack Creation: get_stack_status function in change_testbed_params.py file did not return any thing"
                break
        fi
        done
	echo " Final List of all Heat Stacks "
	heat stack-list 
	python /root/$1/inp_to_yaml.py /root/$1/input.json create_cluster_json > /root/$1/cluster.json
	echo "cluster.json now Created"
	python /root/$1/inp_to_yaml.py /root/$1/input.json create_server_json > /root/$1/server.json
	echo "server.json now Created"
	python /root/$1/inp_to_yaml.py /root/$1/input.json get_sm_ip > /root/$1/server-manager-file
	echo "server-manager-file now created that conatins server manager IP"
	python /root/$1/inp_to_yaml.py /root/$1/input.json get_config_node_ip > /root/$1/config-node-ip
	echo "config-node-ip file now created that contains config node IP"
	python /root/$1/inp_to_yaml.py /root/$1/input.json create_testbedpy_file > /root/$1/testbed.py
	echo "Testbed.py file created that will be used for running the tests on the overlay cluster"
	echo " -----   DONE  -----"

else
        echo "Network Stack Creation failed. So creation of the SERVER STACK is TERMINATED !!!!"
fi
