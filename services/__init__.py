from .gdtot import GDTOTService
from .filepress import FilePressService
from .hubdrive import HubDriveService

# Service factory
def get_service(service_name):
    services = {
        "gdtot": GDTOTService,
        "filepress": FilePressService,
        "hubdrive": HubDriveService
    }
    
    service_class = services.get(service_name)
    if service_class:
        return service_class()
    return None 