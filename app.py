from browsermobproxy import Server
from selenium import webdriver

PROXY = "bmp:9090" # IP:PORT or HOST:PORT

#webdriver.DesiredCapabilities.CHROME['proxy'] = {
#    "httpProxy": PROXY,
#    "ftpProxy": PROXY,
#    "sslProxy": PROXY,
#    "proxyType": "MANUAL",
#}

#webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True

breakpoint()

server = Server('/browsermob-proxy-2.1.4/bin/browsermob-proxy')
server.start()
proxy = server.create_proxy()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--proxy-server={proxy.proxy}')
chrome_options.add_argument(f'--headless')
chrome_options.add_argument(f'--disable-gpu')
chrome_options.add_argument(f'--no-sandbox')


driver = webdriver.Chrome(options=chrome_options)

proxy.new_har("google")
res = driver.get("http://innergrandslowstars.neverssl.com/online/")
print(proxy.har) # returns a HAR JSON blob

driver.quit()
