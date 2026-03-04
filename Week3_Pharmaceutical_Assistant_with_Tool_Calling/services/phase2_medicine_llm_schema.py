"""
LLM Tool Definitions in JSON Schema Format
Defines the tools available for the LLM to query medicine information from both the local database and the OpenFDA API. 
Each tool includes a name, description, and JSON schema for input parameters.
"""


MEDICINE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_medicine_info",
            "description": "Find medicine information by brand name or generic name...",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "The medicine brand name or generic name..."
                    }
                },
                "required": ["search_term"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "drug_lookup",
            "description": "Query the OpenFDA API for drug label information...",
            "parameters": {
                "type": "object",
                "properties": {
                    "generic_name": {
                        "type": "string",
                        "description": "The generic name of the drug to look up..."
                    }
                },
                "required": ["generic_name"]
            }
        }
    }
]