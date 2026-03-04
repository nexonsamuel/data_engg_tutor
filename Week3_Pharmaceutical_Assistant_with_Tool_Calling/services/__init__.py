"""Services Package

This package provides utilities and services for API interactions and database management.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

# Import main services/modules for easier access
from .openfda_api import drug_lookup
from .medicine_dbutil import insert_medicines_from_csv,  get_medicine_info
from .interactions_dbutil import insert_interactions_from_json, check_drug_interaction
from .comprehensive_drug_dbutil import insert_comprehensive_drugs_from_csv, get_drugs_by_class, get_drug_details
from .phase3_medicine_llm_schema import MEDICINE_TOOLS

__all__ = [
    "drug_lookup",
    "insert_medicines_from_csv",
    "get_medicine_info",
    "insert_interactions_from_json",
    "check_drug_interaction",
    "insert_comprehensive_drugs_from_csv",
    "get_drugs_by_class",
    "get_drug_details",
    "MEDICINE_TOOLS"
]