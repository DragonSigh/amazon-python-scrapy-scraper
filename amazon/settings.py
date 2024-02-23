
BOT_NAME = 'amazon'

SPIDER_MODULES = ['amazon.spiders']
NEWSPIDER_MODULE = 'amazon.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

SCRAPEOPS_API_KEY = 'YOUR_API_KEY'

SCRAPEOPS_PROXY_ENABLED = False
# SCRAPEOPS_PROXY_SETTINGS = {'country': 'us'}

# Add In The ScrapeOps Monitoring Extension
#EXTENSIONS = {
#'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
#}

LOG_LEVEL = 'INFO'

#DOWNLOADER_MIDDLEWARES = {

    ## ScrapeOps Monitor
#    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
#    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    
    ## Proxy Middleware
#    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
#}

# Max Concurrency On ScrapeOps Proxy Free Plan is 1 thread
CONCURRENT_REQUESTS = 1

AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 90
AUTOTHROTTLE_DEBUG = True

DOWNLOAD_DELAY = 2

FEED_EXPORTERS = {
    'xlsx': 'scrapy_xlsx.XlsxItemExporter',
}

DEFAULT_REQUEST_HEADERS = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
     'Content-Type': 'application/x-www-form-urlencoded',
     'Connection': 'keep-alive',
     'Accept-Encoding': 'gzip, deflate',
     'Accept-Language': 'en-US,en;q=0.5'
 }
 