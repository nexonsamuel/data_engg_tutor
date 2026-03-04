import requests
import json
from typing import Dict


def drug_lookup(generic_name: str):
    """
    Query the OpenFDA API to retrieve drug label information by generic name.
    Returns a dictionary with status, brand_name, generic_name, active_ingredients,
    purpose, indications, and warnings.
    """

    print("Inside the drug_lookup function")
    BASE_URL = "https://api.fda.gov/drug/label.json"

    # Clean and format the generic name for the query
    input_generic_name = generic_name.strip()
    query = f'openfda.generic_name:"{input_generic_name}"'

    params = {
        "search": query,
        "limit": 2
    }
    
    # Make the API request
    print(f"Querying OpenFDA API for generic name: {input_generic_name}")
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            print("Successfully retrieved data from OpenFDA API")
            
            try:
                results_info = response.json().get("results", [])
            except requests.exceptions.JSONDecodeError:
                print("Error parsing JSON response from OpenFDA API")
                return {"error": "Failed to parse API response"}
            
            if not results_info:
                return {"error": f"No results found for generic name: {input_generic_name}"}
            else:
                active_ingredients = results_info[0].get("active_ingredient", [])
                extracted_brand_name = results_info[0].get("openfda", {}).get("brand_name", ["N/A"])[0]
                generic_name = results_info[0].get("openfda", {}).get("generic_name", ["N/A"])[0]
                purpose = results_info[0].get("purpose", ["N/A"])[0]
                indications = results_info[0].get("indications_and_usage", ["N/A"])[0]
                warnings = results_info[0].get("warnings", ["N/A"])[0]
                response_dict = {
                    "brand_name": extracted_brand_name,
                    "generic_name": generic_name,
                    "active_ingredients": active_ingredients,
                    "purpose": purpose,
                    "indications": indications,
                    "warnings": warnings
                }
            return response_dict
        else:
            print(f"Failed to retrieve data from OpenFDA API. Status code: {response.status_code}")
            return {"error": f"API request failed with status code: {response.status_code}"}
        
    except requests.exceptions.Timeout:
        print("Request to OpenFDA API timed out")
        return {"error": f"Request timeout while querying for generic name: {input_generic_name}"}
    except requests.exceptions.ConnectionError:
        print("Connection error while querying OpenFDA API")
        return {"error": f"Connection error while querying for generic name: {input_generic_name}"}
    except requests.exceptions.RequestException as e:
        print(f"Error querying OpenFDA API: {e}")
        return {"error": f"Failed to retrieve data for generic name: {input_generic_name}"}