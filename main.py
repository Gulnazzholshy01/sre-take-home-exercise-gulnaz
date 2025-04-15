import yaml
import requests
import time
from collections import defaultdict
from urllib.parse import urlparse

# Function to load configuration from the YAML file
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        if not isinstance(config, list):
            raise ValueError("Invalid configuration format: Expected a list of endpoints.")
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Unable to parse YAML file: {e}")
        sys.exit(1)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=0.5)  
        response_time = (time.time() - start_time) * 1000  

        if 200 <= response.status_code < 300 and response_time <= 500:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"
    

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        start_time = time.time()

        for endpoint in config:
            domain = urlparse(endpoint["url"]).netloc.split(":")[0]  
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"]) if stats["total"] > 0 else 0
            print(f"{domain} has {availability}% availability percentage")
            
        print("---")
        elapsed_time = time.time() - start_time
        time.sleep(max(0, 15 - elapsed_time))

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")