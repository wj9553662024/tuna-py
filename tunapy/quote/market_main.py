""" Market Main
"""
import os
import sys
from logging import Logger

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURR_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import common.jpm_config as jpm_config
from common.configer import Configer
from common.utils.log_utils import create_logger
from quote.bn_public_ws import create_market_data as bn_pubws
from quote.gate_public_ws import create_market_data as gate_pubws
from quote.jc_public_ws import create_market_data as jc_pubws
from quote.mexc_public_ws import create_market_data as mexc_pubws
from quote.bitmart_public_ws import create_market_data as bitmart_pubws
from quote.gate_alpha_quote import alpha_quote


def _create_bn_ws(tokens: list):
    topics, log_name = [], 'BNSPOT-PubWS'
    for symbol in tokens:
        symbol = symbol.lower()
        topics.append(f'{symbol}@depth20@100ms')
        if jpm_config.COMBINE_USDS:
            if symbol[-1] == 't':
                topics.append(f'{symbol[:-1]}c@depth20@100ms')
            else:
                topics.append(f'{symbol[:-1]}t@depth20@100ms')
        topics.append(f'{symbol}@aggTrade')
    logger = create_logger(CURR_DIR, "quoter.log", log_name, backup_cnt=10)
    logger.info('Topcis: %s', topics)
    bn_pubws(topics)

def _create_gate_ws(tokens: list):
    """ create market client subscribing public websocket
    """
    log_name = 'GATESPOT-PubWS'
    topics = [symbol.upper() for symbol in tokens]
    logger = create_logger(CURR_DIR, "quoter.log", log_name, backup_cnt=10)
    logger.info('Topcis: %s', topics)
    gate_pubws(topics)

def _create_jc_ws(tokens: dict):
    """ create market client subscribing public websocket
    """
    log_name = 'JUSPOT-PubWS'
    topics = list(tokens.keys())
    logger = create_logger(CURR_DIR, "quoter.log", log_name, backup_cnt=10)
    logger.info('Topcis: %s', topics)
    jc_pubws(topics, logger)

def _create_mexc_ws(tokens: list):
    """ create market client subscribing public websocket
    """
    log_name = 'MEXCSPOT-PubWS'
    topics = [symbol.upper() for symbol in tokens]
    logger = create_logger(CURR_DIR, "quoter.log", log_name, backup_cnt=10)
    logger.info('Topcis: %s', topics)
    mexc_pubws(topics)

def _create_bitmart_ws(tokens: list):
    """ create market client subscribing public websocket
    """
    log_name = 'BITMARTSPOT-PubWS'
    topics = [symbol.upper() for symbol in tokens]
    logger = create_logger(CURR_DIR, "quoter.log", log_name, backup_cnt=10)
    logger.info('Topcis: %s', topics)
    bitmart_pubws(topics)

def _create_alpha_rest(tokens: dict):
    """ create gate alpha market client polling tickers
    """
    log_name = 'GateAlpha-Rest'
    logger = create_logger(CURR_DIR, "quoter.log", log_name, backup_cnt=10)
    logger.info('Tokens: %s', tokens)
    alpha_quote(tokens, logger)


def main():
    """ main workflow of market data
        symbols.append('jasmyusdt@depth20@100ms')
        symbols.append('jasmyusdt@aggTrade')
    """
    if len(sys.argv) != 2:
        print(f'python3 {sys.argv[0]} <APP_NAME>')
        return

    app_name = sys.argv[1]
    configer = Configer(app_name)
    quote_config = configer.get_config()

    if jpm_config.MAIN_QUOTE_EXCHANGE == jpm_config.EXCHANGE_BN:
        _create_bn_ws(quote_config['TOKENS'])
    elif jpm_config.MAIN_QUOTE_EXCHANGE == jpm_config.EXCHANGE_GATE:
        _create_gate_ws(quote_config['TOKENS'])
    elif jpm_config.MAIN_QUOTE_EXCHANGE == jpm_config.EXCHANGE_MEXC:
        _create_mexc_ws(quote_config['TOKENS'])
    elif jpm_config.MAIN_QUOTE_EXCHANGE == jpm_config.EXCHANGE_BITMART:
        _create_bitmart_ws(quote_config['TOKENS'])
    elif jpm_config.MAIN_QUOTE_EXCHANGE == jpm_config.EXCHANGE_OKX:
        log_name = 'OKXSPOT-PubWS'
    elif jpm_config.MAIN_QUOTE_EXCHANGE == jpm_config.EXCHANGE_JU:
        _create_jc_ws(quote_config['TOKENS'])
    elif jpm_config.MAIN_QUOTE_EXCHANGE == jpm_config.EXCHANGE_GATE_ALPHA:
        _create_alpha_rest(quote_config['TOKENS'])
    else:
        return

    #get_market_client(MAIN_QUOTE_EXCHANGE, quote_config['TOKENS'])
    #get_market_client(BACKUP_QUOTE_EXCHANGE, topics)


if __name__ == '__main__':
    main()
