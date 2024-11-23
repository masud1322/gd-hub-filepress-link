import os

# API Configuration
config = {
    # GDTOT Configuration
    "gdtot": {
        "domain": os.getenv('GDTOT_DOMAIN', 'https://new7.gdtot.dad'),
        "cookies": {
            "crypt": os.getenv('GDTOT_CRYPT'),
            "PHPSESSID": os.getenv('GDTOT_PHPSESSID')
        }
    },
    
    # Simplified FilePress Configuration
    "filepress": {
        "domain": os.getenv('FILEPRESS_DOMAIN', 'https://new1.filepress.top'),
        "api_key": os.getenv('FILEPRESS_API_KEY')
    },
    
    # GDFlix Configuration
    "gdflix": {
        "domain": "",
        "api_key": "",
        "cookies": {}
    },
    
    # HubDrive Configuration
    "hubdrive": {
        "domain": os.getenv('HUBDRIVE_DOMAIN', 'https://hubdrive.my'),
        "cookies": {
            "crypt": os.getenv('HUBDRIVE_CRYPT'),
            "PHPSESSID": os.getenv('HUBDRIVE_PHPSESSID')
        }
    }
}

# Helper functions
def get_gdtot_config():
    return config["gdtot"]

def get_filepress_config():
    return config["filepress"]

def get_gdflix_config():
    return config["gdflix"] 