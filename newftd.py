import os
import requests
import json
import logging

# Logging setup
logging.basicConfig(filename='fmc_add_ftd.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# Configuration file
CONFIG_FILE = 'config.json'

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def authenticate(fmc_ip, username, password):
    try:
        logging.debug(f"Attempting to authenticate with FMC at {fmc_ip}")
        url = f"https://{fmc_ip}/api/fmc_platform/v1/auth/generatetoken"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, auth=(username, password), headers=headers, verify=False)
        response.raise_for_status()
        headers['X-auth-access-token'] = response.headers['X-auth-access-token']
        logging.debug("Authentication successful")
        print("Authentication successful")
        return headers
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to authenticate: {e}")
        print(f"Failed to authenticate: {e}")
        return None

def get_domains(headers, fmc_ip):
    try:
        logging.debug("Retrieving domains from FMC")
        url = f"https://{fmc_ip}/api/fmc_platform/v1/info/domain"
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        domains = response.json()
        logging.debug("Domains retrieved successfully")
        print("Domains retrieved successfully")
        return domains
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve domains: {e}")
        print(f"Failed to retrieve domains: {e}")
        return None

def add_ftd_device(headers, fmc_ip, domain_uuid, device_name, device_ip):
    try:
        logging.debug(f"Adding FTD device {device_name} with IP {device_ip} to domain {domain_uuid}")
        url = f"https://{fmc_ip}/api/fmc_config/v1/domain/{domain_uuid}/devices/devicerecords"
        payload = {
            "name": device_name,
            "hostName": device_ip,
            "type": "Device",
            "ftdMode": "true"
        }
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        logging.info(f"Successfully added FTD device {device_name}")
        print(f"Successfully added FTD device {device_name}")
    except requests.exceptions.HTTPError as e:
        error_message = get_error_message(response)
        logging.error(f"Failed to add FTD device {device_name}: HTTP {response.status_code} - {error_message}")
        print(f"Failed to add FTD device {device_name}: HTTP {response.status_code} - {error_message}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to add FTD device {device_name}: {e}")
        print(f"Failed to add FTD device {device_name}: {e}")

def get_error_message(response):
    if response.status_code == 400:
        return "Bad Request - The server could not understand the request due to invalid syntax."
    elif response.status_code == 401:
        return "Unauthorized - Authentication is required and has failed or has not yet been provided."
    elif response.status_code == 403:
        return "Forbidden - The client does not have access rights to the content."
    elif response.status_code == 404:
        return "Not Found - The server can not find the requested resource."
    elif response.status_code == 422:
        return "Unprocessable Entity - The server understands the content type of the request entity, but was unable to process the contained instructions."
    elif response.status_code == 500:
        return "Internal Server Error - The server has encountered a situation it doesn't know how to handle."
    else:
        return f"{response.reason}"

def main():
    try:
        print(f"Current Working Directory: {os.getcwd()}")
        with open(CONFIG_FILE, 'r') as file:
            config_content = file.read()
            #Remove # below to see config printed if getting stuck
            #print(f"Raw Config Content: {config_content}")
            config = json.loads(config_content)
        
        fmc_ip = config['fmc_ip']
        username = config['username']
        password = config['password']
        devices_to_add = config['ftd_devices']
        
        headers = authenticate(fmc_ip, username, password)
        if headers:
            domains = get_domains(headers, fmc_ip)
            if domains:
                print("Available Domains:")
                for index, domain in enumerate(domains['items']):
                    print(f"{index + 1}. Domain Name: {domain['name']}, Domain UUID: {domain['uuid']}")
                selected_index = int(input("Enter the number of the domain to use: ")) - 1
                selected_domain_uuid = domains['items'][selected_index]['uuid']
                
                for device in devices_to_add:
                    add_ftd_device(headers, fmc_ip, selected_domain_uuid, device['name'], device['ip'])
            else:
                logging.error("No domains retrieved")
                print("No domains retrieved")
        else:
            logging.error("Script terminated due to authentication failure")
            print("Script terminated due to authentication failure")
    except FileNotFoundError:
        logging.error(f"Configuration file {CONFIG_FILE} not found")
        print(f"Configuration file {CONFIG_FILE} not found")
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing configuration file {CONFIG_FILE}: {e}")
        print(f"Error parsing configuration file {CONFIG_FILE}: {e}")
    except ValueError:
        logging.error("Invalid input for domain selection")
        print("Invalid input for domain selection")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
