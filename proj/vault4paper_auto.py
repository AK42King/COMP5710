from http import client
from pathlib import Path
from itertools import count
import os
import re
import shutil
from venv import create
import hvac 
import random 



'''

1. Install Vault 



- `brew tap hashicorp/tap` 

- `brew install hashicorp/tap/vault` 



2. Verify the HCP Vault installation: 



- `vault` 



3. Start the HCP Vault server. This will help us to programmatically store secrets 



- `vault server -dev` 



4. Keep an eye on the output of `vault server -dev` . From the output we will use `address` and `token` 



5. `pip install hvac`

'''



counter_mapper           = {}

hvac_token               = "hvs.Str5ggGdums2yaLtYKBiwxPX" ## this should come from the output of *vault server -dev* 

hvac_url                 = "http://127.0.0.1:8200"        ## this should come from the output of *vault server -dev*

ansible_secret_retrieval = '"{{ lookup(' + "'hashi_vault', 'secret=secret/data/"  

puppet_secret_retrieval  = "Deferred('vault_lookup::lookup', ["  




def makeConn():

    hvc_client = hvac.Client(url= hvac_url, token= hvac_token) 

    return hvc_client 

def storeSecret( client,  secr1 , cnt  ):

    secret_path     = 'SECRET_PATH_' + str( cnt  )

    create_response = client.secrets.kv.v2.create_or_update_secret(path=secret_path, secret=dict(password =  secr1 ) )

    # print( type( create_response ) )

    # print( dir( create_response)  )



def retrieveSecret(client_, cnt_, tech_str): 

    secret_path        = 'SECRET_PATH_' + str( cnt_  )

    read_response      = client_.secrets.kv.read_secret_version(path=secret_path, raise_on_deleted_version=False) 

    secret_from_vault  = read_response['data']['data']['password']

    # print('The secret we have obtained:')

    print("To retrieve the secret '{}' please plugin the following code snippet in your script:".format( secret_from_vault) )

    if tech_str == 'A': 

        # print(secret_path)

        # print(ansible_secret_retrieval)

        print(ansible_secret_retrieval + secret_path + " token=" + hvac_token + " url=" + hvac_url + "')['password'] }}" + '"')

    elif tech_str == 'P':

        # print(puppet_secret_retrieval + '"' + secret_path + '/' + hvac_token  + '", ' + hvac_url + "']),"  )

        print(puppet_secret_retrieval + '"' + secret_path + '/' + hvac_token  + '", \'' + hvac_url + "']),"  )







def preprocessTechInput(tech_str):

    str2ret = ''

    tech_str = tech_str.replace('\n', '')

    tech_str = tech_str.replace('\r', '')    



    str2ret  = tech_str 

    return str2ret





def storeSecrets(lis_secr, tech_str): 

    clientObj    =  makeConn() 

    for secret2store in lis_secr: 

        counter = random.randint(1, 100000)

        storeSecret( clientObj,   secret2store, counter )

        counter_mapper[counter] = tech_str

    print("Finished storing secrets!")

    print('='*50)    





def retrieveSecrets( tech_str ): 

    clientObj = makeConn() 

    for counter, v_ in counter_mapper.items():

        retrieveSecret( clientObj,  counter, tech_str )

    print('='*50)

def auto_process_files(base_path, tech_str):
    client = makeConn()
    secret_keywords = ['password', 'secret', 'token', 'key', 'admin', 'access', 'private', 'salt']
    pattern = re.compile(rf"(?i)^(\s*)([\w\-\.]+):\s+['\"]?(.+?)['\"]?$")

    # Create a folder to save updated files
    processed_path = os.path.join(base_path, "processedAn")
    os.makedirs(processed_path, exist_ok=True)

    for root, _, files in os.walk(base_path):
        for fname in files:
            if tech_str == 'A' and fname.endswith(".yml"):
                fpath = os.path.join(root, fname)
                new_lines = []
                with open(fpath, 'r', encoding='utf-8') as file:
                    for line in file:
                        match = pattern.match(line)
                        if match:
                            indent, var, value = match.groups()
                            if any(k in var.lower() for k in secret_keywords):
                                # store the value in Vault
                                counter = random.randint(1, 100000)
                                storeSecret(client, value, counter)
                                vault_ref = (
                                    ansible_secret_retrieval +
                                    f"SECRET_PATH_{counter} token={hvac_token} url={hvac_url}')['password'] }}"
                                )
                                line = f"{indent}{var}: {vault_ref}\n"
                        new_lines.append(line)

                # Write the processed file
                rel_path = os.path.relpath(fpath, base_path)
                dest_file = os.path.join(processed_path, rel_path)
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                with open(dest_file, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
    
    print("Finished auto-processing all YAML files and replacing secrets.")




if __name__ == '__main__': 

    print("Welcome!")

    print("This Python program will ask for inputs from you in order to store secrets and provide code to retrieve secrets.")

    print("First let's understand what technology are you using? Type 'A' for Ansible and 'P' for Puppet:")

    technology_string = input()

    preprocessTechInput( technology_string )

    print("Thanks. Please provide the secrets that you want this program to securely store:")

    inp_secret_holder = []

    while True: 

        print("Please provide the secret that you want the program to secure. Hit 'q' to quit:")

        secret = input() 

        secret = preprocessTechInput(secret)

        if secret == 'Q' or secret == 'q': 

            break

        inp_secret_holder.append( secret  )

    storeSecrets( inp_secret_holder, technology_string )

    print("Do you want the code snippet to retrieve your secrets? 'Y' for yes and 'N' for no.")

    retrieve = input()

    retrieve = preprocessTechInput( retrieve )

    if retrieve == 'Y' or retrieve == 'y': 

        retrieveSecrets( technology_string )

    elif retrieve == 'N' or retrieve == 'n': 

        print("Thanks for using the program. Goodbye!")

    print("Do you want to auto-process YAML files and store/replace secrets? Y/N")
    autoproc = input().strip()
    if autoproc.upper() == 'Y':
        print("Enter the directory path to scan (e.g. './secrets_extracted'):")
        path = input().strip()
        auto_process_files(path, technology_string)



