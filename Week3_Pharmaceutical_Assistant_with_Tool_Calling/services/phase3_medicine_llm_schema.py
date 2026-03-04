"""
LLM Tool Definitions in JSON Schema Format

Comprehensive tool definitions for Phase 2 and Phase 3.
Includes tools for medicine info, drug lookups, interactions, alternatives, and comparisons.
Compatible with Claude, ChatGPT, and other LLM APIs.
"""

MEDICINE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_medicine_info",
            "description": "Find medicine information by brand name or generic name from local database. Returns up to 5 matching results with manufacturer, uses, and side effects.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "The medicine brand name or generic name to search for (e.g., 'Aspirin', 'Ibuprofen')"
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
            "description": "Query the OpenFDA API for drug label information including warnings, indications, active ingredients, and side effects using the generic drug name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "generic_name": {
                        "type": "string",
                        "description": "The generic name of the drug to look up (e.g., 'Aspirin', 'acetylsalicylic acid')"
                    }
                },
                "required": ["generic_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_drug_interactions",
            "description": "Check for known drug-drug interactions between two medications. Returns interaction severity (Major/Moderate/Minor), mechanism, clinical effects, safer alternatives, and management recommendations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "drug_a": {
                        "type": "string",
                        "description": "The first drug name (e.g., 'Warfarin', 'Aspirin')"
                    },
                    "drug_b": {
                        "type": "string",
                        "description": "The second drug name (e.g., 'Ibuprofen', 'Naproxen')"
                    }
                },
                "required": ["drug_a", "drug_b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_therapeutic_alternatives",
            "description": "Find therapeutic alternatives for a given drug. Returns other drugs in the same therapeutic class with their indications, side effects, dosage forms, and availability (OTC/Prescription).",
            "parameters": {
                "type": "object",
                "properties": {
                    "drug_name": {
                        "type": "string",
                        "description": "The drug name to find alternatives for (e.g., 'Aspirin', 'Ibuprofen')"
                    }
                },
                "required": ["drug_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_drugs",
            "description": "Compare multiple drugs side-by-side. Returns detailed information on each drug including indications, side effects, dosage, route of administration, availability, and contraindications for easy comparison.",
            "parameters": {
                "type": "object",
                "properties": {
                    "drug_list": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of drug names to compare (e.g., ['Aspirin', 'Ibuprofen', 'Naproxen'])"
                    }
                },
                "required": ["drug_list"]
            }
        }
    }
]