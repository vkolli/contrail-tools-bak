import sys
import json
from fabric.api import *
import paramiko
import os
import subprocess
import ast
import uuid
import random
import string 

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
testbed_py_dict = parsed_json["inp_params"]["testbed_py_params"]


for i in network_dict:
	network_name_list.append(network_dict[i]["name"])
	# A list to maintain all the network names 		

# A method for generating random names for the project name
def generate_random_name():
	size = 10
	chars = string.ascii_uppercase + string.digits
	print ''.join(random.choice(chars)for x in range(size))


# A method for adding the project UUID in the names of the of all the networks so that they won't create duplicates 
def change_network_dict():
	project_uuid = general_params_dict["project_uuid"]
	#print project_uuid
	for k in network_dict:
                if project_uuid not in k:
			new_key = k+"_"+project_uuid
                	network_dict[new_key] = network_dict.pop(k)
	#print network_dict
	for i in network_dict:
		name = network_dict[i]["name"]
		if project_uuid not in name:
			new_name = name+"_"+project_uuid
			network_dict[i]["name"] = new_name
	#print network_dict

# A Method for chnaginf the network and the server stack names 
def change_stack_names():
	project_uuid = general_params_dict["project_uuid"]
	general_params_dict["network_stack_name"] = general_params_dict["network_stack_name"]+project_uuid
	general_params_dict["server_stack_name"] = general_params_dict["server_stack_name"]+project_uuid

# A method to create a yaml file to create networks using the heat component of the openstack 
def create_network_yaml():
	change_network_dict()
	project_uuid = general_params_dict["project_uuid"]
	network_string = ""
	network_string = network_string+"heat_template_version: 2015-04-30\n\ndescription: "+description+"\n\n" + "resources:\n"
	for i in network_dict:
		num = 1
		if "name" in network_dict[i]:
			name = network_dict[i]["name"]
		else:
			name = i
		network_name_list.append(name)
		network_string = network_string + "  "+name+":\n"
		network_string = network_string + "    type: OS::Neutron::Net\n"
		network_string = network_string + "    properties:\n      name: "+name+"\n"
		network_string = network_string + "      tenant_id: %s\n\n"%project_uuid
		subnet_name = name+"_subnet_"+str(num)
 		network_string = network_string + "  "+subnet_name+":\n"
		network_string = network_string + "    type: OS::Neutron::Subnet\n"
		network_string = network_string + "    properties:\n"
		network_string = network_string + "      tenant_id: %s\n"%project_uuid
		network_string = network_string + "      network_id: { get_resource: %s }\n"%name
		ip_block_with_mask = network_dict[i]["ip_block_with_mask"]
		network_string = network_string + "      cidr: %s\n"%ip_block_with_mask
		network_string = network_string + "      ip_version: 4\n"
		network_string = network_string + "      name: %s\n\n"%subnet_name
		num = num+1
	print network_string



# A Method for changing the server_dict according to the given 'project_uuid' given in the 'input.json' file so that naming complications can be avoided.
def change_server_dict():
	project_uuid = general_params_dict["project_uuid"]
	#print server_dict	
	for i in server_dict:
		if project_uuid not in i:
			new_key = i+"_"+project_uuid
			server_dict[new_key] = server_dict.pop(i)
	'''
	for i in server_dict:
		name = server_dict[i]["name"]
		if project_uuid not in name:
			new_name = name+"_"+project_uuid
			server_dict[i]["name"] = new_name
	'''
	#print server_dict
	for i in server_dict:
		a= server_dict[i]['ip_address']
		for j in a:
			if project_uuid not in j:
				new_key  = j+"_"+project_uuid
				a[new_key] = a.pop(j)
	#print server_dict	

# A Method for changing the floatingIP pool parameters from the input.json
def change_floatingip_pool_params():
	project_uuid = general_params_dict["project_uuid"]
	name = floating_ip_network_dict["param"]["name"]
	if project_uuid not in name:
		new_name = name+"_"+project_uuid
		floating_ip_network_dict["param"]["name"] = new_name 
	return floating_ip_network_dict

# A Method to create a yaml file to create servers using the heat component of the openstack 
def create_server_yaml():
	port_string = ""
	server_string = ""
	server_string = server_string+"heat_template_version: 2015-04-30\n\ndescription: "+description+"\n\n" + "resources:\n"
	ip_port_dict = {}
	# Change the contents of the Server_dict 
	change_server_dict()
	#Change the contets of the Network_dict 
	change_network_dict()
	#Change the contents Cluster Names 
	change_stack_names()
	#Change the contents of the floating_ip_network_dict
	floating_ip_network_dict = change_floatingip_pool_params()
	# Create required ports for all the VMs
	for i in server_dict:
		#print server_dict[i]
		name = server_dict[i]["name"]
		# The internal dictionary that contains the mapping of the network name to the fixed ip should also be chnaged. The next 5 lines are doing that
		ip_address_dict = server_dict[i]["ip_address"]
		project_uuid = general_params_dict["project_uuid"]
		for k in ip_address_dict:
			new_key = k+"_"+project_uuid
			#ip_address_dict[new_key] = ip_address_dict.pop(k)
		#print ip_address_dict
		#ip_num = 0
		for j in network_dict:
			if network_dict[j]["role"] == "management":
                                ip_num = 0
                        else:
                                ip_num = 1
			net_name = network_dict[j]["name"]
			port_name = name + "_port_" + str(ip_num)
			server_string = server_string + "  "+port_name+":\n"
			server_string = server_string + "    type: OS::Neutron::Port\n"
			server_string = server_string + "    properties:\n"
			server_string = server_string + "      network: %s\n"%net_name
			server_string = server_string + "      name: %s\n"%port_name
			if "mac_address" in server_dict[i]:
				server_string = server_string + "      mac_address: %s\n"%(server_dict[i]["mac_address"][net_name]) 
			server_string = server_string + "      fixed_ips:\n"
			server_string = server_string + "        - ip_address: %s\n"%ip_address_dict[net_name]
			if network_dict[j]["role"] == "management":
				if ("external_vip" in cluster_dict["parameters"]["provision"]["openstack"]):
					server_string = server_string + "      allowed_address_pairs:\n"
					server_string = server_string + "        - ip_address: %s\n\n"%cluster_dict["parameters"]["provision"]["openstack"]["external_vip"]
			if network_dict[j]["role"] == "control-data":
				if ("internal_vip" in cluster_dict["parameters"]["provision"]["openstack"]):
					server_string = server_string + "      allowed_address_pairs:\n"
					server_string = server_string + "        - ip_address: %s\n\n"%cluster_dict["parameters"]["provision"]["openstack"]["internal_vip"]
			ip_port_dict[(ip_address_dict[net_name])] = port_name
			#ip_num += 1
	# Launch the VMs
	ip_association_floating = []
	for i in server_dict:
		name = server_dict[i]["name"]
		server_string = server_string + "  "+name+":\n"
		server_string = server_string + "    type: OS::Nova::Server\n"
		server_string = server_string + "    properties:\n      name: "+name+"\n"
		server_string = server_string + "      flavor: %s\n"%server_dict[i]["flavor"]
		server_string = server_string + "      image: %s\n"%server_dict[i]["image"]
		server_string = server_string + "      networks:\n"
		port_for_floating_ip = []
		ip_address_dict = server_dict[i]["ip_address"]
		ip_list = ip_address_dict.values()
		#print ip_list[1]
		for key, value in ip_address_dict.items():
			if value in ip_list:
				if network_dict[key]["role"] == "management":
					ip_association_floating.append(value)
					server_string = server_string + "        - port: { get_resource:  %s}\n"%ip_port_dict[value]
					ip_list.remove(value)
		if len(ip_list) > 0:
			#print ip_association_floating	
			for j in ip_list:
				#print ip_list
				server_string = server_string + "        - port: { get_resource:  %s}\n"%ip_port_dict[j]
				if len(port_for_floating_ip) == 0:
					port_for_floating_ip.append(ip_port_dict[j])
			server_string = server_string + "\n"
	# If Floating IP Pool present in the given Json tanslate it into the yaml file 
	if "floating_ip_network" in parsed_json["inp_params"]:
		# Change the name of the floatingip pool. Add the porject uuid to the name.
		change_floatingip_pool_params()
		name = floating_ip_network_dict["param"]["name"]
		server_string = server_string + "  "+name+":\n"
		server_string = server_string + "    type: OS::ContrailV2::FloatingIpPool\n"
		server_string = server_string + "    properties:\n"
		server_string = server_string + "      name: %s\n"%name
		server_string = server_string + "      virtual_network: %s\n\n"%floating_ip_network_dict["param"]["floating_ip_network_uuid"]
		#server_string = server_string + "      virtual_network: public\n\n"
	#creating floating IP from the above created pool for the VMs
	for i in server_dict:
		if server_dict[i]["floating_ip"] == "true":
                	name = server_dict[i]["name"]+"_floating_ip"
			server_string = server_string + "  "+name+":\n"
			server_string = server_string + "    type: OS::ContrailV2::FloatingIp\n"
			server_string = server_string + "    properties:\n"
			#floating_ip = server_dict[i]["floating_ip"]
			#server_string = server_string + "      floating_ip_address: %s\n"%floating_ip
			abc = ip_association_floating[0]
			port_to_associate = ip_port_dict[abc]
			#print ip_port_dict
			#print port_to_associate
			ip_association_floating.pop(0)
			#server_string = server_string + "      virtual_machine_interface_refs: [{ get_resource : %s}]\n"%port_for_floating_ip[0]
			server_string = server_string + "      virtual_machine_interface_refs: [{ get_resource : %s}]\n"%port_to_associate
			floating_ip_network_dict = parsed_json["inp_params"]["floating_ip_network"]["param"] 
			server_string = server_string + "      floating_ip_pool: { get_resource: %s }\n"%floating_ip_network_dict["name"]
			server_string = server_string + "      floating_ip_fixed_ip_address: %s \n"%abc
			server_string = server_string + "      project_refs: [ %s ]\n\n"%general_params_dict["project_uuid"]
                else:
                        pass
		
	print server_string
	#print ip_association_floating


# Method for Parsing Openstack Resource output
fixed_ip_mac_mapping = {}
#Dict for storing fixed IP to Mac mapping
#floating_ip_mac_mapping is for the mapping of the floating ip to the server manager VM so that it can be used in the provisioning of the server manager vm
floating_ip_mac_mapping = {}
def parse_output():
	project_uuid = general_params_dict["project_uuid"] 
	# Change the contents of the Server_dict 
        change_server_dict()
        #Change the contets of the Network_dict 
        change_network_dict()
        #Change the contents of the floating_ip_network_dict
        floating_ip_network_dict = change_floatingip_pool_params()
	#Change both the stack names
	change_stack_names()
	network_stack_name = general_params_dict["network_stack_name"]
	server_stack_name = general_params_dict["server_stack_name"]
	#print network_stack_name
	#print server_stack_name 
	all_server_names = []
	for i in server_dict:
                name = server_dict[i]["name"]
		#name = name+"_"+ project_uuid
		all_server_names.append(name)
	#print all_server_names
	#print server_stack_name
	for i in all_server_names:
		#a = os.system("openstack stack resource show %s %s"%(server_stack_name,i))
		a = subprocess.Popen("openstack stack resource show %s %s"%(server_stack_name,i), shell=True ,stdout=subprocess.PIPE)
		a_tmp = a.stdout.read()
		a_tmp = str(a_tmp)
		#print a_tmp
		split_list_1 = a_tmp.split("attributes")
		#print split_list_1
		split_string_1 = split_list_1[1]
		#print split_string_1
		split_list_2 = split_string_1.split("creation_time")
		#print split_list_2[0]
		split_string_2 = split_list_2[0]
		split_list_3 = split_string_2.split("|")
		#print split_list_3
		final_string = split_list_3[1]
		final_string.replace(" ","")
		#print final_string
		# Convert the above string 'final_string' into a valid dictionary
		final_resource_params_dict = eval(final_string)
		#print final_resource_params_dict["addresses"]
		for j in final_resource_params_dict["addresses"]:
			#print j
			for k in range (len(final_resource_params_dict["addresses"][j])):
				#print k	
				#print final_resource_params_dict["addresses"][j]
				if final_resource_params_dict["addresses"][j][k]["OS-EXT-IPS:type"]=="fixed":
					fixed_ip_mac_mapping[final_resource_params_dict["addresses"][j][k]["addr"]] = final_resource_params_dict["addresses"][j][k]["OS-EXT-IPS-MAC:mac_addr"]
					#print "Yes"
				elif final_resource_params_dict["addresses"][j][k]["OS-EXT-IPS:type"] == "floating":
					floating_ip_mac_mapping[final_resource_params_dict["addresses"][j][k]["OS-EXT-IPS-MAC:mac_addr"]] = final_resource_params_dict["addresses"][j][k]["addr"]
	#print fixed_ip_mac_mapping
	#print floating_ip_mac_mapping


# A Method for gettinf the server manager ip
def get_sm_ip():
	a = subprocess.Popen('neutron floatingip-list -f json',shell=True ,stdout=subprocess.PIPE)
	a_tmp = a.stdout.read()
	a_tmp = str(a_tmp)
	fip_neutron_dict = eval(a_tmp)
	floating_ip = ""
	change_network_dict()
	net_name = []
	for i in network_dict:
		net_name.append(network_dict[i]["name"])
	for i in server_dict:
		if server_dict[i]["server_manager"] == "true":
			for j in server_dict[i]["ip_address"]:
				for k in range(len(fip_neutron_dict)):
					if fip_neutron_dict[k]["fixed_ip_address"] == server_dict[i]["ip_address"][j]:
						b = subprocess.Popen('neutron port-show %s -f json'%fip_neutron_dict[k]["port_id"],shell=True ,stdout=subprocess.PIPE)
						b_tmp = b.stdout.read()
						b_tmp = str(b_tmp)
						current_port_dict = json.loads(b_tmp)
						current_network_id = current_port_dict["network_id"]
						c = subprocess.Popen('neutron net-list -f json',shell=True ,stdout=subprocess.PIPE)
						c_tmp = c.stdout.read()
						c_tmp = str(c_tmp)
						all_net_dict  = json.loads(c_tmp)
						for net in all_net_dict:
							if current_network_id == net["id"] and net["name"] in net_name:
								floating_ip = fip_neutron_dict[k]["floating_ip_address"]
	print floating_ip

# Method for getting the floating ip of the config node so that the testbed.py can be transferred to this server and the tests can run from here.
def get_config_node_ip():
	"""
	parse_output()
	config_node_ip = ""
	for i in server_dict:
		if server_dict[i]["server_manager"] != "true":
			if "config" in server_dict[i]["roles"]:
				for j in server_dict[i]["ip_address"]:
					private_ip = server_dict[i]["ip_address"][j]
					private_mac = fixed_ip_mac_mapping[private_ip]
					if private_mac in floating_ip_mac_mapping:
						config_node_ip = floating_ip_mac_mapping[private_mac]
	print config_node_ip
	"""
	a = subprocess.Popen('neutron floatingip-list -f json',shell=True ,stdout=subprocess.PIPE)
        a_tmp = a.stdout.read()
        a_tmp = str(a_tmp)
        fip_neutron_dict = eval(a_tmp)
	project_uuid = general_params_dict["project_uuid"]
        config_node_ip = ""
	change_network_dict()
	net_name = []
	for i in network_dict:
                net_name.append(network_dict[i]["name"])
        for i in server_dict:
		if server_dict[i]["server_manager"] != "true":
			if "config" in server_dict[i]["roles"]:
				for j in server_dict[i]["ip_address"]:
					for k in range(len(fip_neutron_dict)):
						if fip_neutron_dict[k]["fixed_ip_address"] == server_dict[i]["ip_address"][j]:
							b = subprocess.Popen('neutron port-show %s -f json'%fip_neutron_dict[k]["port_id"],shell=True ,stdout=subprocess.PIPE)
                                                	b_tmp = b.stdout.read()
                                                	b_tmp = str(b_tmp)
                                                	current_port_dict  = json.loads(b_tmp)
							current_network_id = current_port_dict["network_id"]
							c = subprocess.Popen('neutron net-list -f json',shell=True ,stdout=subprocess.PIPE)
							c_tmp = c.stdout.read()
							c_tmp = str(c_tmp)
							all_net_dict  = json.loads(c_tmp)
							for net in all_net_dict:
								if current_network_id == net["id"] and net["name"] in net_name:
									config_node_ip = fip_neutron_dict[k]["floating_ip_address"]
	print config_node_ip
					
# Method for creating the server json required for adding the servers to the server manager 
def create_server_json():
	parse_output()
	# Change the contents of the Server_dict 
        #change_server_dict()
        #Change the contets of the Network_dict 
        change_network_dict()
        #Change the contents of the floating_ip_network_dict
        floating_ip_network_dict = change_floatingip_pool_params()
	#Change the Cluster Names
	change_stack_names()
	server_json_string = '''{
	"server":[
	'''
	# Call the parse_output function os that we can use the IP-Mac Mapping provided by the function 
	#parse_output()
	mac_address_list= []
	for i in fixed_ip_mac_mapping:
		mac_address_list.append(fixed_ip_mac_mapping[i])
	#print mac_address_list
	"""
	for i in mac_address_list:
		if i in floating_ip_mac_mapping:
			ipmi_ip = floating_ip_mac_mapping[i]
	"""
	#print ipmi_ip
	total_server_number = len(parsed_json["inp_params"]["servers"]) -1
	for i in server_dict:
		if server_dict[i]["server_manager"] != "true":
			"""
			for j in server_dict[i]["ip_address"]:
				private_ip = server_dict[i]["ip_address"][j]
				private_mac = fixed_ip_mac_mapping[private_ip]
				if private_mac in floating_ip_mac_mapping:
					ipmi_ip = floating_ip_mac_mapping[private_mac]
			"""
			single_server_string = '''
			{
			"cluster_id": "%s",
			"contrail": {
				"control_data_interface": "%s"
			},
			"host_name": "%s",
			"id": "%s",
			"domain": "%s",
			"network": {
			'''%(cluster_dict["cluster_id"], cluster_dict["control_data_iterface"], server_dict[i]["name"], server_dict[i]["name"], cluster_dict["parameters"]["domain"])
			single_server_string = single_server_string + '''       "interfaces": ['''
			total_server_interfaces = len(parsed_json["inp_params"]["servers"][i]["ip_address"]) 
			for j in (server_dict[i]["ip_address"]):
				current_network = j
				gateway = network_dict[j]["default_gateway"]
				ip_add = server_dict[i]["ip_address"][j]
				mask = network_dict[j]["ip_block_with_mask"]
				mask_list = mask.split("/")
				mask = mask_list[1]
				mac_address = fixed_ip_mac_mapping[ip_add]
				role = network_dict[j]["role"]
				if role == "management":
					int_name = cluster_dict["management_interface"]
				else:
					int_name = cluster_dict["control_data_iterface"]
				if total_server_interfaces > 1:
					single_server_string = single_server_string + '''
					{
						"default_gateway": "%s",
						"dhcp": false,
						"ip_address": "%s/%s",
						"mac_address": "%s",
						"name": "%s"
					},
					'''%(gateway, ip_add, mask, mac_address, int_name)
				else:
					single_server_string = single_server_string + '''
	                                {
	                                        "default_gateway": "%s",
	                                        "dhcp": false,
	                                        "ip_address": "%s/%s",
	                                        "mac_address": "%s",
	                                        "name": "%s"
	                                }
	                                '''%(gateway, ip_add, mask, mac_address, int_name)
				total_server_interfaces = total_server_interfaces - 1
			single_server_string = single_server_string +"],"
			single_server_string = single_server_string +'\n			"management_interface": "%s"\n'%(cluster_dict["management_interface"])
			server_json_string = server_json_string + single_server_string
			server_json_string_contd = '''
			},
			"password": "%s",
			"roles": [
			'''%(cluster_dict["server_password"])
			roles_string = ''
			total_number_of_roles = len(server_dict[i]["roles"])
			for j in server_dict[i]["roles"]:
				if total_number_of_roles > 1:
					roles_string = roles_string + '	"%s",\n'%j
				else:
					roles_string = roles_string + ' "%s"\n'%j
				total_number_of_roles = total_number_of_roles - 1
			server_json_string = server_json_string + server_json_string_contd
			server_json_string = server_json_string + roles_string
			#print single_server_string
			# Is the number of servers in the input.json is more than one then we need commas in the json after every server dict.
			if total_server_number > 1:	
				server_json_string_contd = '''
				]
				},
				'''
				total_server_number =total_server_number - 1
			else:
				server_json_string_contd = '''
	                        ]
	                        }
	                        '''
			# Reduce the number of the total servers by one so that when we insert the last server dict in the json file, it will not include the comma (,) at the end 
			server_json_string = server_json_string + server_json_string_contd
	closing_string = '''
	]
}
	'''
	server_json_string = server_json_string + closing_string
	print server_json_string


# Method for creating cluster json for the server manager
def create_cluster_json():
        #Change the Cluster Names 
        change_stack_names()
        cluster_json_string = ''' {
    "cluster": [
        {
            "id": "%s",
            "parameters": {
                "domain": "%s",
                "provision": {
                    "contrail": {
                        "database": {
                            "minimum_diskGB": %d
                        },
			“amqp_ssl” : true,
                        "kernel_upgrade": %s
                    },
        '''%(cluster_dict["cluster_id"], cluster_dict["parameters"]["domain"], cluster_dict["parameters"]["provision"]["contrail"]["minimum_disk_database"], cluster_dict["parameters"]["provision"]["contrail"]["kernel_upgrade"])

	if (("external_vip" in cluster_dict["parameters"]["provision"]["openstack"]) and ("internal_vip" in cluster_dict["parameters"]["provision"]["openstack"])):
		cluster_json_string = cluster_json_string +'''
		"openstack": {
			"keystone": {
				"admin_password" : "c0ntrail123"		
			},
                        "ha": {
                            "external_vip": "%s",
                            "external_virtual_router_id": %d,
                            "internal_vip": "%s",
                            "internal_virtual_router_id": %d
                        }
                    }
                }
            }
        }
    ]
}		
		'''%(cluster_dict["parameters"]["provision"]["openstack"]["external_vip"], cluster_dict["parameters"]["provision"]["openstack"]["external_virtual_router_id"], cluster_dict["parameters"]["provision"]["openstack"]["internal_vip"], cluster_dict["parameters"]["provision"]["openstack"]["internal_virtual_router_id"])
	else:
		cluster_json_string = cluster_json_string + '''
			"openstack": {
				"keystone": {
					"admin_password": "c0ntrail123"
				}
			}
		 }
            }
        }
    ]
}
		'''
	print cluster_json_string

def create_testbedpy_file():
	file_str = ""
        file_str = file_str + "from fabric.api import env \n\next_routers = []\nrouter_asn = 64512\n\n"
        itr = 1
        # hostname_string contains the hostanme of all the servers. This would be added to the main string after wards
        hostname_string = "     'all' : [ "
        build_ip = ""
	control_data_string = "control_data = {\n"
	name_mapping = {}
	if "env_password" in testbed_py_dict:
		env_password_string = "\nenv.passwords = {\n"
	if "env_ostypes" in testbed_py_dict:
		env_ostypes_string = "env.ostypes = {\n"
	for i in server_dict:
                if server_dict[i]["server_manager"] != "true":
                        for j in server_dict[i]["ip_address"]:
                                if network_dict[j]["role"] == "management":
                                        if "config" in server_dict[i]["roles"]:
                                                # Build Ip that will be used in the testbed.py file
						if "host_build" in testbed_py_dict:
							build_ip = testbed_py_dict["host_build"]
						else:
                	                                build_ip = server_dict[i]["ip_address"][j]
                                        manag_ip = server_dict[i]["ip_address"][j]
                                else:
					if network_dict[j]["role"] == "control-data":
						# control data ip that will be used in the control-data section of the testbed.py file
						control_ip = server_dict[i]["ip_address"][j]
						gateway = network_dict[j]["default_gateway"]
					else:
						continue
                        for net in network_dict:
				if network_dict[net]["role"] == 'control-data':
					control_data_string = control_data_string + "   host%s : { 'ip': '%s', 'gw' : '%s', 'device': 'eth1'},\n"%(str(itr), control_ip, gateway)
                        file_str = file_str + "host%s = 'root@%s'\n"%(str(itr),manag_ip)
			if "env_password" in testbed_py_dict:
				env_password_string = env_password_string + "   host%s: '%s',\n"%(str(itr), testbed_py_dict["env_password"])
			if "env_ostypes" in testbed_py_dict:
				env_ostypes_string = env_ostypes_string + "     host%s: '%s',\n"%(str(itr), testbed_py_dict["env_ostypes"])
			# logic for not adding ',' (comma) after the last hostname in the env.hostname field of the testbed.py being created.
                        if itr == len(server_dict) - 1:
                                hostname_string = hostname_string + "'" +(server_dict[i]["name"]) + "' "
				testbed_py_name = "host%s"%str(itr)
				name_mapping[server_dict[i]["name"]] = testbed_py_name
                        else:
                                hostname_string = hostname_string + "'" +(server_dict[i]["name"]) + "', "
				testbed_py_name = "host%s"%str(itr)
                                name_mapping[server_dict[i]["name"]] = testbed_py_name
                        itr += 1
	hostname_string = hostname_string + "]\n"
	control_data_string = control_data_string + "}\n\n"
	role_per_server_mapping = {"all":[], "cfgm":[], "openstack":[], "webui":[], "control":[], "collector":[], "database":[], "compute":[], "build":["host_build"]}
	if "env_ostypes" in testbed_py_dict:
		env_ostypes_string = env_ostypes_string + "}\n\n"
	if "env_password" in testbed_py_dict:
		env_password_string = env_password_string + "   host_build: '%s',\n}\n\n"%testbed_py_dict["env_password"]
		file_str = file_str + "\nenv.password = '%s'\n"%testbed_py_dict["env_password"]
	file_str = file_str + "host_build = 'root@%s'\n\n"%build_ip
	# Lets Get the role definitions for all the servers in the input file
	# All the hostnames for env.roles section in testbed.py file
	all_host_list = name_mapping.values()
	for i in all_host_list:
		role_per_server_mapping["all"].append(i)
	for i in server_dict:
		if server_dict[i]["server_manager"] != "true":
			if "config" in server_dict[i]["roles"]:
				role_per_server_mapping["cfgm"].append(name_mapping[server_dict[i]["name"]])
			if "openstack" in server_dict[i]["roles"]:
				role_per_server_mapping["openstack"].append(name_mapping[server_dict[i]["name"]])
			if "webui" in server_dict[i]["roles"]:
				role_per_server_mapping["webui"].append(name_mapping[server_dict[i]["name"]])
			if "control" in server_dict[i]["roles"]:
				role_per_server_mapping["control"].append(name_mapping[server_dict[i]["name"]])		
			if "collector" in server_dict[i]["roles"]:
				role_per_server_mapping["collector"].append(name_mapping[server_dict[i]["name"]])
			if "database" in server_dict[i]["roles"]:
				role_per_server_mapping["database"].append(name_mapping[server_dict[i]["name"]])	
			if "compute" in server_dict[i]["roles"]:
				role_per_server_mapping["compute"].append(name_mapping[server_dict[i]["name"]])
	file_str = file_str + "env.hostnames = {\n"
	file_str = file_str + hostname_string + "}\n\n"
	file_str = file_str + "env.interface_rename = False\n\n"
	for net in network_dict:
		if network_dict[net]["role"] == "control-data":
			file_str = file_str + control_data_string
	# Print all the role defs referenced from the 'role_per_server_mapping' dict mention above 	
        file_str = file_str + "env.roledefs = {\n"
	#itr = len(role_per_server_mapping)
	itr = 1
        for i in role_per_server_mapping:
		#inner_iter = len(role_per_server_mapping[i])
		inner_iter = 1
		file_str = file_str +"	'%s' : [ "%i
		for j in role_per_server_mapping[i]:
			if inner_iter == len(role_per_server_mapping[i]):
				file_str = file_str + j + " ]"
			else:
				file_str = file_str + "%s, "%j
			inner_iter += 1
		if itr == len(role_per_server_mapping):
			file_str = file_str + "\n"
		else:
			file_str = file_str + ",\n"
		itr += 1
	file_str = file_str + "}\n\n"

	if "openstack_admin_password" in testbed_py_dict:
		file_str = file_str + "env.openstack_admin_password = '%s'\n"%testbed_py_dict["openstack_admin_password"]
	if "env_password" in testbed_py_dict:
		file_str = file_str + env_password_string
	if "env_ostypes" in testbed_py_dict:
		file_str = file_str + env_ostypes_string
	if (("external_vip" in cluster_dict["parameters"]["provision"]["openstack"]) and ("internal_vip" in cluster_dict["parameters"]["provision"]["openstack"])):
		file_str = file_str+"ha_setup = True\n"
		file_str = file_str + "env.ha = {\n"
		file_str = file_str+"	'internal_vip' : '%s',\n"%cluster_dict["parameters"]["provision"]["openstack"]["internal_vip"]
		file_str = file_str+"	'external_vip' : '%s'\n}\n\n"%cluster_dict["parameters"]["provision"]["openstack"]["external_vip"]	
	file_str = file_str + "env.cluster_id='%s'\n"%cluster_dict["cluster_id"]
	if "minimum_diskGB" in testbed_py_dict:
		file_str = file_str + "minimum_diskGB = %d\n"%testbed_py_dict["minimum_diskGB"]
	if "env.test_repo_dir" in testbed_py_dict:
		file_str = file_str + "env.test_repo_dir= '%s'\n"%testbed_py_dict["env.test_repo_dir"]
	if "env.mail_from" in testbed_py_dict:
		file_str = file_str + "env.mail_from= '%s'\n"%testbed_py_dict["env.mail_from"]
	if "env.mail_to" in testbed_py_dict:
		file_str = file_str + "env.mail_to= '%s'\n"%testbed_py_dict["env.mail_to"]
	if "multi_tenancy" in testbed_py_dict:
		file_str = file_str + "multi_tenancy= %s\n"%testbed_py_dict["multi_tenancy"]
	if "env.interface_rename" in testbed_py_dict:
		file_str = file_str + "env.interface_rename = %s\n"%testbed_py_dict["env.interface_rename"]
	if "env.encap_priority" in testbed_py_dict:
		file_str = file_str + 'env.encap_priority = "%s"\n'%testbed_py_dict["env.encap_priority"]
	if "env.enable_lbaas" in testbed_py_dict:
		file_str = file_str + "env.enable_lbaas = %s\n"%testbed_py_dict["env.enable_lbaas"]
	if "enable_ceilometer" in testbed_py_dict:
		file_str = file_str + "enable_ceilometer = %s\n"%testbed_py_dict["enable_ceilometer"]
	if "ceilometer_polling_interval" in testbed_py_dict:
		file_str = file_str + "ceilometer_polling_interval = %d\n"%testbed_py_dict["ceilometer_polling_interval"]
	if "do_parallel" in testbed_py_dict:
		file_str = file_str + "do_parallel = %s\n"%testbed_py_dict["do_parallel"]	
	print file_str	
		
			
											

if __name__ == '__main__':
	globals()[sys.argv[2]]()

"""
Imp Points to Remember: 

FLAVORS USED :
-----------------
openstack flavor list 
+----+------------+-------+------+-----------+-------+-----------+
| ID | Name       |   RAM | Disk | Ephemeral | VCPUs | Is Public |
+----+------------+-------+------+-----------+-------+-----------+
| 1  | m1.tiny    |   512 |    1 |         0 |     1 | True      |
| 2  | m1.small   |  2048 |   20 |         0 |     1 | True      |
| 3  | m1.medium  |  4096 |   40 |         0 |     2 | True      |
| 4  | m1.large   |  8192 |   80 |         0 |     4 | True      |
| 5  | m1.xlarge  | 16384 |  160 |         0 |     8 | True      |
| 6  | m1.xxlarge | 32768 |  300 |         0 |    10 | True      |
+----+------------+-------+------+-----------+-------+-----------+

IMAGES USED:
---------------
ubuntu-14.04-server-cloudimg-amd64-disk1.img  -- 256 MB  

create_network_yaml:
---------------------
 The name parameter in the input json file is optional. If you dont put in the name, the script will by default take the key from the network dictionary that is created.

create_server_yaml:
-------------------- 
-> If you don't want to attach a floating IP to the Virtual machine, dont add the "floating_ip" field in the individual server dict.
-> If you don't intend to attach a Floating IP to any of your machine, in addition to doing the above setp, don't add the "floating_ip_network" field to the the "inp_params" dict. This will not create the flo
ating IP pool required to the setup.
-> Also make sure to change the name of the FIP pool in the input json for every heat stack. So that they do not interfer with each other.(There can be multiple FIPs attached to a particular network)
"""

