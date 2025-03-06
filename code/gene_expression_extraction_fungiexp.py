import os
import time
import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

# Custom adapter to force TLSv1.2
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        pool_kwargs['ssl_version'] = ssl.PROTOCOL_TLSv1_2
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       **pool_kwargs)

# Create a session and mount the custom adapter for HTTPS
session = requests.Session()
session.mount('https://', TLSAdapter())

# Define Taxon IDs and Base URL
taxon_ids = ["948595", "498257", "100787", "683960", "742152", "5421", "1333698", "1365886", "336722"]
base_url = "https://bioinfo.njau.edu.cn/fungiExp/"

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Install ChromeDriver using WebDriver Manager
service = Service(ChromeDriverManager().install())

for taxon_id in taxon_ids:
    # Define the download folder for the current taxon
    download_folder = os.path.join(os.getcwd(), taxon_id)
    
    # If directory already exists, skip this taxon ID to avoid duplication
    if os.path.exists(download_folder):
        print(f"Directory for taxon {taxon_id} already exists. Skipping.")
        continue
    # Create the folder if it does not exist
    os.makedirs(download_folder)
    
    # Initialize WebDriver for the current taxon
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the website
    url = f"{base_url}info.php?taxonId={taxon_id}"
    driver.get(url)

    # Wait for JavaScript to load the page
    time.sleep(5)

    all_gene_expr_links = []

    while True:
        # Extract Gene Expression download links on the current page
        gene_expr_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'fileType=exptGeneExpr')]")
        for link in gene_expr_links:
            relative_url = link.get_attribute("href")
            # Ensure it's a full URL by joining with base URL
            full_url = urljoin(base_url, relative_url)
            all_gene_expr_links.append(full_url)

        # Try to find the "Next" button
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            if "disabled" in next_button.get_attribute("class"):
                break
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(5)
            next_button.click()
            time.sleep(5)
        except Exception:
            break  # No more pages

    # Close browser after collecting links
    driver.quit()

    # Download each file with correct naming
    for file_url in all_gene_expr_links:
        # Extract the filename from the "datasource" parameter (which defines the file)
        if "datasource=" in file_url:
            file_id = file_url.split("datasource=")[-1]
            file_name = f"{file_id}.gene.expr.tsv"
        else:
            file_name = "unknown.tsv"  # Fallback name

        file_path = os.path.join(download_folder, file_name)

        # Define a common User-Agent header to mimic a browser
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            # Use the session with the custom TLS adapter and headers
            response = session.get(file_url, headers=headers, verify=False)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"Downloaded: {file_name}")
            else:
                print(f"Failed to download: {file_name} (status code: {response.status_code})")
        except Exception as e:
            print(f"Error downloading {file_name}: {e}")

    print(f"\nAll files downloaded for taxon {taxon_id}\n")
