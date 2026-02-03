import os
import sys
import json
import threading
import time
import asyncio

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURR_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
JUMP_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
if JUMP_DIR not in sys.path:
    sys.path.insert(0, JUMP_DIR)

from okx.websocket.WsPublicAsync import WsPublicAsync
from octopuspy.utils.log_util import create_logger
# from utils.config_util import set_config

FIVE_MIN_HUNDRED_MS = 5*600
    
PUBLIC_STREAM = 'wss://ws.okx.com:8443/ws/v5/public'  #For public data like market tickers, order books, etc.
PRIVATE_STREAM = 'wss://ws.okx.com:8443/ws/v5/private' #For private data like account updates, order notifications, etc.
APP_NAME = 'okx_marketing'
APP_LOGGER = create_logger('./', f'{APP_NAME}.log', APP_NAME, 100)
MESSAGE_TIMEOUT = 30 

class OkxAsyncPubWs:
    def __init__(self, symbols=["BTC-USDT"], base_url=PUBLIC_STREAM, logger=APP_LOGGER):
        self.url = base_url
        self._force_stop = False
        self.ws = WsPublicAsync(self.url)
        self.symbols = symbols
        self.logger = logger
        self._order_book = {}
        self._book_message_buff = {}
        self._last_message_ts = time.time()
        for symbol in self.symbols:
            self._order_book[symbol] = {}
            self._book_message_buff[symbol] = []
        
            
    # depth: 401 ~ 10000
    # default: 500    
    def full_order_book(self):
        for symbol in self.symbols:
            try:
                self._order_book[symbol] = full_orderbook(symbol)
            except Exception as e:
                self.logger.error(traceback.format_exc())
        
        
    def _on_message(self, message):
        try:
            j = json.loads(message)
            self.process_message(j)
            self._last_message_ts = time.time()
        except Exception as e:
            self.logger.error("error message: %s" % message)
            self.logger.error(traceback.format_exc())
            
    
    def process_message(self, j):
        if j.get('event') and j['event'] == "error":
            self.logger.error("error event: %s " % j)
            #print("error event: %s " % j)'event': 'subscribe'
        elif j.get('event') and j['event'] == "subscribe":
            self.logger.debug("message subscribe: %s " % j)
        elif j.get('arg') and j['arg'].get('channel'):
            channel = j['arg']['channel']
            if channel == 'tickers':
                print("ticker: ", j['arg'])
                self.process_ticker(j)
                #TODO：caculate ts, create key, save to redis
            elif channel == 'books':
                print("books: ", j['arg'])
                self.process_book(j)
                #TODO：caculate ts, create key, save to redis
            elif channel == 'trades':
                print("trades: ", j['arg'])
                self.process_trade(j)
                #TODO：to be defined
            else:
                print("non processing: message", j)
        else:
            print("non processing: message", j)            
            
    
    def process_book(self, j):
        #self.logger.debug("processing book message: %s" % j)
        if j['action'] == 'snapshot':
            self.init_orderbook(j)
        elif j['action'] == 'update':
            self.update_orderbook(j)
        else:
            self.logger.error("orderbook unhandled message: %s" % j)


    def update_orderbook(self, j):
        symbol = j['arg']['instId']
        self._book_message_buff[symbol].append(j)   # another thread will processing the message buffer
        merge_ob_thread = threading.Thread(target=merge_ob_fun, args=(self, symbol, self.logger))
        merge_ob_thread.start()
        merge_ob_thread.join()


    def init_orderbook(self, j):
        symbol = j['arg']['instId']
        if not self._order_book.get(symbol):
            self._order_book[symbol] = {}
        self._order_book[symbol]['asks'] = {}
        self._order_book[symbol]['bids'] = {}
        
        for price, qty, _, _ in j['data'][0]['asks']:
            self._order_book[symbol]['asks'][price] = qty
        for price, qty, _, _ in j['data'][0]['bids']:
            self._order_book[symbol]['bids'][price] = qty
        self._order_book[symbol]['seqId'] = j['data'][0]['seqId']
        self._order_book[symbol]['prevSeqId'] = j['data'][0]['prevSeqId']
        self._order_book[symbol]['ts'] = int(j['data'][0]['ts'])
        self.logger.debug('init order book with snapshot: %s, %s' % (symbol, self._order_book[symbol]))


    def process_ticker(self, j):
        self.logger.debug("processing ticker message: %s" % j)
        ts = j['data'][0]['ts']
        last_price = j['data'][0]['last']
        symbol = j['arg']['instId']
        self.logger.debug(f'last price of {symbol} is {last_price} at time {ts}')
        #print("processing ticker message: %s" % j)

    def process_trade(self, j):
        self.logger.debug("processing trade message: %s" % j)
        #print("processing trade message: %s" % j)

    def _create_args(self):
        args = []
        for symbol in self.symbols:
            args.append(
                {
                    "channel": "trades",
                    "instId": symbol
                }
            )
            args.append(
                {
                    "channel": "tickers",
                    "instId": symbol
                },
            )
            args.append(
                {
                    "channel": "books",
                    "instId": symbol
                }
            )
        debug_msg=f'subscribe args: {args}'
        self.logger.debug(debug_msg)
        return args
    
        
    async def _run(self):
        try:
            await self.ws.start()
            args = self._create_args()
            await self.ws.subscribe(args, callback=self._on_message)
            while not self._force_stop:
                ts = time.time()
                print(f"last message: {ts - self._last_message_ts} s" )
                if ts > self._last_message_ts + MESSAGE_TIMEOUT:
                    self._force_stop = True
                    break
                await asyncio.sleep(1)
            await self.ws.unsubscribe(args, callback=self._on_message)
        except Exception as e:
            self._force_stop = True
            self.logger.error(traceback.format_exc())

    # restart
    async def _run_run(self):
        while 1:
            self._force_stop = False
            self.logger.debug('connect and run!')
            await self._run()
            await asyncio.sleep(1)
            

    def run_forever(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run_run())

    async def _stop(self):
        self._force_stop = True
        self.logger.debug('processing is stoping!')

    async def _restart(self):
        self.logger.debug('processing restarting!')
        self._force_stop = False
        self.run_forever()

def get_msg_time_info(ob):
    try:
        seqId = ob['seqId']
        prevSeqId = ob['prevSeqId']
        ob_ts = float(ob['ts'])
        return seqId, prevSeqId, ob_ts
    except Exception as e:
        print(e)
        return "-2", "-3", 0
    

def _key(tag, ts):
    """ BiNance Spot
        The update period of Binance WS is 100ms.
        5 minutes have 5 * 60 * 10 = 3000 (100ms)
    """
    return f'okxsd{tag}{ts % FIVE_MIN_HUNDRED_MS}'


def merge_ob_fun(client: OkxAsyncPubWs, symbol: str, logger):
    ob = client._order_book[symbol]
    #print("ob before merge thread: %s" % ob)
    id1, prevId1, obTs1 = get_msg_time_info(ob)
    msg_buff = client._book_message_buff[symbol]
    t1 = time.time()
    l1 = len(msg_buff)
    while len(msg_buff) > 0:
        did_something = False
        for ob_msg in msg_buff:
            id2, prevId2, obTs2 = get_msg_time_info(ob_msg['data'][0])
            if obTs2 < int(obTs1):
                logger.debug('skip book update: %s' % ob_msg)
                logger.debug('skip book update: %s < %s' % (obTs2, obTs1))
                msg_buff.remove(ob_msg)
                did_something = True
                break
            elif prevId2 == id1:     # msg next to last orderbook update
                ob['seqId'] = id2
                ob['prevSeqId'] = prevId2
                ob['ts'] = obTs2
                #logger.debug('merge book update: %s' % ob_msg)
                sorted_asks, sorted_bids = merge_ask_bid(ob, ob_msg['data'][0])
                #logger.debug('after merge, order_book: %s' % ob)
                msg_buff.remove(ob_msg)
                did_something = True
                break
        if not did_something:
            logger.debug(f"warning: no book message matched in a loop for symbol {symbol}! wait 0.1 second.")
            time.sleep(0.1)
    t2 = time.time()
    logger.debug(f'thread ended for processing book message of {symbol}. before processing: {l1}messages, after processing: {len(msg_buff)}. time consumed: {t2-t1}s')
    
    
def merge_ask_bid(ob_data, update_data):
    asks: dict = ob_data['asks']
    #print("asks before merge: ", asks)
    #update_ts = ob_data['ts']
    for price, qty, _, _ in update_data['asks']:
        if float(qty) == 0:
            del asks[price]
        else:
            asks[price] = qty
    sorted_asks = sorted(asks.items(), key=lambda x: float(x[0]), reverse=False)
    
    bids: dict = ob_data['bids']
    for price, qty, _, _ in update_data['bids']:
        if qty == 0:
            del bids[price]
        else:
            bids[price] = qty
    sorted_bids = sorted(bids.items(), key=lambda x: float(x[0]), reverse=True)
    return sorted_asks, sorted_bids


        
if __name__ == '__main__':
    okx = OkxAsyncPubWs(symbols=['BTC-USDT'])
    okx.run_forever()
