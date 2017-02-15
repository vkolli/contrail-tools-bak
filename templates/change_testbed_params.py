import sys
import json
import os
import subprocess


#with open("floating_ip_test_multiple.json") as json_data:
if (sys.argv[1]=='-h' or sys.argv[1]=='--help'):
        print '''
        THE CORRECT FORMAT OF USING THIS SCRIPT IS:
                python inp_to_yaml.py <input_json_file> <function_to_perform>
        EXAMPLE :
                python inp_to_yaml.py input.json create_network_yaml > network.yaml
        '''
        sys.exit()

inp_file = sys.argv[1]
with open(inp_file) as json_data:
        parsed_json = json.load(json_data)


description = parsed_json["inp_params"]["description"]["msg"]
total_servers = parsed_json["inp_params"]["params"]["no_of_servers"]
total_networks = parsed_json["inp_params"]["params"]["no_of_networks"]

network_name_list=[]
#parse all the data from the json file into a dict so that it an be used in the script 

# Creating all The Dictionaries from the input json file that are required for all the functions to work properly in a scalable manner
server_dict = parsed_json["inp_params"]["servers"]
network_dict = parsed_json["inp_params"]["networks"]
cluster_dict = parsed_json["inp_params"]["cluster_json_params"]
floating_ip_network_dict = parsed_json["inp_params"]["floating_ip_network"]
general_params_dict = parsed_json["inp_params"]["params"]

# Method for changing the testbed.py file for the new cluster.
def change_testbed_params():
        #print sys.argv[2]
        path_to_testbed = sys.argv[2]
        management_server_ip_mapping = {}
        control_server_ip_mapping = {}
        for i in server_dict:
                if server_dict[i]["server_manager"] != "true":
                        ip_add_dict = server_dict[i]["ip_address"]
                        for j in ip_add_dict:
                                if network_dict[j]["role"] == "management":
                                        keyname = i + "_ip_manage"
                                        management_server_ip_mapping[keyname]=ip_add_dict[j]
                                else:
                                        keyname = i + "_ip_control"
                                        control_server_ip_mapping[keyname] = ip_add_dict[j]
        #print management_server_ip_mapping
        #print control_server_ip_mapping
        for i in network_dict:
                if network_dict[i]["role"] == "control-data":
                        control_data_gateway = network_dict[i]["default_gateway"]
                        os.system("sed -i 's/control_data_gateway/%s/' %s"%(control_data_gateway, path_to_testbed))
        #print control_data_gateway
        externalvip = ""
        internalvip = ""
        if "external_vip" in cluster_dict["parameters"]["provision"]["openstack"]:
                externalvip = cluster_dict["parameters"]["provision"]["openstack"]["external_vip"]
                os.system("sed -i 's/externalvip/%s/' %s"%(externalvip, path_to_testbed))
        if "internal_vip" in cluster_dict["parameters"]["provision"]["openstack"]:
                internalvip = cluster_dict["parameters"]["provision"]["openstack"]["internal_vip"]
                os.system("sed -i 's/internalvip/%s/' %s"%(internalvip, path_to_testbed))
        #print externalvip
        #print internalvip
        for i in management_server_ip_mapping:
                os.system("sed -i 's/%s/%s/' %s"%(i, management_server_ip_mapping[i], path_to_testbed))
        for i in control_server_ip_mapping:
                os.system("sed -i 's/%s/%s/' %s"%(i, control_server_ip_mapping[i], path_to_testbed))


if __name__ == '__main__':
	globals()[sys.argv[3]]()
