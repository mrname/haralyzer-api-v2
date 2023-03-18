from browsermobproxy import Server
from selenium import webdriver


def create_har_data(url, name=None) -> dict:
    """
    Given a single URL, this function will generate a dict of raw HAR data
    using BrowserMobProxy and Selenium
    """
    # Necessary, or HTTPS will not work at all
    webdriver.DesiredCapabilities.CHROME["acceptSslCerts"] = True

    server = Server("/browsermob-proxy-2.1.4/bin/browsermob-proxy")
    server.start()
    proxy = server.create_proxy()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--proxy-server={proxy.proxy}")
    chrome_options.add_argument(f"--headless")
    chrome_options.add_argument(f"--disable-gpu")
    chrome_options.add_argument(f"--no-sandbox")
    # We could mount /dev/shm from the host instead technically, it is likely to be
    # faster
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    proxy.new_har(name or "default")
    driver.get(url)
    driver.quit()
    return proxy.har
