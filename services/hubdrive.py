import requests
import re
from bs4 import BeautifulSoup
from config import config

class HubDriveService:
    def __init__(self):
        self.config = config["hubdrive"]
        self.domain = self.config["domain"]
        self.cookies = self.config["cookies"]
    
    def convert_link(self, drive_link):
        """Convert Google Drive link to HubDrive link"""
        try:
            # First get the upload page to get any required tokens
            session = requests.Session()
            session.cookies.update({
                "crypt": self.cookies["crypt"],
                "PHPSESSID": self.cookies["PHPSESSID"]
            })
            
            # Get upload page
            upload_url = f"{self.domain}/upload-link"
            session.get(upload_url)
            
            # Now make the API request
            api_url = f"{self.domain}/ajax.php?ajax=upload-link"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html, */*; q=0.01",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": self.domain,
                "Referer": upload_url,
                "X-Requested-With": "XMLHttpRequest"
            }
            
            data = {
                "url": drive_link,
                "ajax": "upload-link"
            }
            
            print("\nHubDrive Request:")
            print(f"URL: {api_url}")
            print(f"Data: {data}")
            
            response = session.post(
                api_url,
                headers=headers,
                data=data,
                timeout=30
            )
            
            print(f"\nHubDrive Response Status: {response.status_code}")
            print(f"Response Text: {response.text[:500]}")
            
            if response.status_code == 200:
                # Try to find the link in different formats
                link_patterns = [
                    r'https://hubdrive\.my/file/\d+',
                    r'class="btn btn-primary".+?href="(.+?)"'
                ]
                
                for pattern in link_patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        hubdrive_link = match.group(1) if 'href' in pattern else match.group(0)
                        
                        # Get file info
                        soup = BeautifulSoup(response.text, 'html.parser')
                        file_info = soup.find('div', {'class': ['filename', 'file-name']})
                        size_info = soup.find('div', {'class': ['filesize', 'file-size']})
                        
                        return {
                            "success": True,
                            "link": hubdrive_link,
                            "service": "hubdrive",
                            "details": {
                                "name": file_info.text.strip() if file_info else "Unknown",
                                "size": size_info.text.strip() if size_info else "Unknown"
                            }
                        }
            
            return {
                "success": False,
                "error": "Could not generate HubDrive link. Please check your cookies.",
                "service": "hubdrive"
            }
            
        except Exception as e:
            print(f"HubDrive Error: {str(e)}")
            return {
                "success": False,
                "error": f"HubDrive Error: {str(e)}",
                "service": "hubdrive"
            } 