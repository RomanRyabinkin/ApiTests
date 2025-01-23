from BaseDirectory.BaseModule import api_version
from Auth.AuthFunctions import random_domain_name
from Auth.AuthFunctions import uncorrect_domain_name

json_for_used_domain = {
    "domain": "lenzaos",
    "version": api_version
}

json_for_unused_domain = {
    "domain": random_domain_name,
    "version": api_version
}

json_for_uncorrected_domain = {
    "domain": uncorrect_domain_name,
    "version": api_version
}

json_for_api_version = {
    "version": api_version
}


