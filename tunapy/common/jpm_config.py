""" JPM Config for Production """
### Constants
EXCHANGE_BN  = 'Binance'
EXCHANGE_GATE = 'Gate'
EXCHANGE_MEXC = 'Mexc'
EXCHANGE_OKX = 'OKX'
EXCHANGE_JU  = 'Jucoin'
EXCHANGE_HFJU  = 'JucoinHF'
EXCHANGE_BIFU  = 'BiFu'
EXCHANGE_MEXC = 'Mexc'
EXCHANGE_BITMART = 'BitMart'
EXCHANGE_BITPORT = 'BitPort'
EXCHANGE_GATE_ALPHA = 'GateAlpha'
EXCHANGE_COINVEX = 'CoinVex'
EXCHANGE_WEEX = 'Weex'


# prefix for distinguishing quote from different exchange
EXCHANGE_BN_DEPTH_PREFIX = 'bnsd'
EXCHANGE_BN_TICKER_PREFIX = 'bnst'
EXCHANGE_GATE_DEPTH_PREFIX = 'gtsd'
EXCHANGE_GATE_TICKER_PREFIX = 'gtst'
EXCHANGE_JU_DEPTH_PREFIX = 'jusd'
EXCHANGE_JU_TICKER_PREFIX = 'just'
EXCHANGE_MEXC_DEPTH_PREFIX = 'mxsd'
EXCHANGE_MEXC_TICKER_PREFIX = 'mxst'
EXCHANGE_BITMART_TICKER_PREFIX = 'bmst'
EXCHANGE_GATEALPHA_DEPTH_PREFIX = 'gasd'
EXCHANGE_GATEALPHA_TICKER_PREFIX = 'gast'

API_REDIS = 'redis'
API_RESTFUL = 'restful'

# sandbox
JUPRE_REST_BASE_URL = 'https://api.jucoin-pre.com'
JUPRE_WS_BASE_URL = 'wss://sws.ju.com/public'

# sandbox BIFU_REST_BASE_URL = 'https://api.bifu.dev'

# product
JU_REST_BASE_URL = 'https://api.jucoin.com'
BN_REST_BASE_URL = 'https://api.binance.com'
BIFU_REST_BASE_URL = 'https://api.bifu.live'
MEXC_REST_BASE_URL = 'https://api.mexc.com'
MEXC_WS_BASE_URL = 'wss://wbs-api.mexc.com/ws'
BITMART_REST_BASE_URL = 'https://api-cloud.bitmart.com'
BITMART_WS_BASE_URL = 'wss://ws-manager-compress.bitmart.com/api?protocol=1.1'
BITPORT_REST_BASE_URL = 'http://spot-gw-internal.bitport.one'
GATEALPHA_REST_BASE_URL = 'https://api.gateio.ws'
WEEX_REST_BASE_URL = 'https://api-spot.weex.com'
WEEX_WS_BASE_URL = 'wss://ws-spot.weex.com/v2/ws/private'

### Configer
CONF_SOURCE = API_REDIS
CONF_POSTFIX = '_jc_'
CONF_SHEET_TOKEN = ''
CONF_SHEET = ''

### Quoter
MAIN_QUOTE_EXCHANGE = EXCHANGE_GATE_ALPHA
BACKUP_QUOTE_EXCHANGE = ''
QUOTE_SOURCE = API_REDIS    # data source
COMBINE_USDS = True     # whether combine USDT and USDC

# the source of mirror quote
EXCHANGE_TICKER_PREFIX = EXCHANGE_MEXC_TICKER_PREFIX
EXCHANGE_DEPTH_PREFIX = EXCHANGE_MEXC_DEPTH_PREFIX

### Market Maker
MM_EXCHANGE = EXCHANGE_HFJU
MM_REST_BASE_URL = JUPRE_REST_BASE_URL
MM_WS_BASE_URL = JUPRE_WS_BASE_URL
BATCH_SIZE = 20

### Self-Trade strategies
ST_STRATEGY = ['random_quantity']
ST_EXCHANGE = EXCHANGE_HFJU
ST_REST_BASE_URL = JUPRE_REST_BASE_URL

### Hedger
HG_MONITOR_HOOK = '675d78cb-4caa-466c-af49-acb7521db204'
HG_EXCHANGE = EXCHANGE_BN
HG_BASE_URL = BN_REST_BASE_URL
