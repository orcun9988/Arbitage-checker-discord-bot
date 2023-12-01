import time
import apprise
import config
import requests


def get_binance_global_fiat_buy_usdt():
    try:
        response = requests.get(config.BINANCE_GLOBAL_BUY_CRYPTO_WITH_FIAT_API)
        response.raise_for_status()
        for crypto in response.json()['data']['cryptoList']:
            if crypto['assetCode'] == 'USDT':
                return float(crypto['quotation'])
    except requests.exceptions.HTTPError as err:
        print(err)
        return None


def get_binance_tr_last_sell_usdt():
    try:
        response = requests.get(config.BINANCE_TR_LAST_SELL_USDT_API)
        response.raise_for_status()
        return float(response.json()["data"]["list"][0]["p"])
    except requests.exceptions.HTTPError as err:
        print(err)
        return None


def message_parser(try_global, try_tr, msg):
    message = config.MESSAGE_TEMPLATE
    key1 = "%message%"
    key2 = "%TRY_GLOBAL%"
    key3 = "%TRY_TR%"
    
    if message.find("%date%") != -1:
        date = time.localtime()
        clock = time.strftime("%H:%M:%S", date)
        day = time.strftime("%d/%m/%Y", date)
        
        message = message.replace("%date%", day + " " + clock)
    
    if msg != "" and message.find(key1) != -1:
        message = message.replace(key1, msg)
    elif msg == "" and message.find(key1) != -1:
        message = message.replace(key1, "") 

    if try_global != "" and message.find(key2) != -1:
        message = message.replace(key2, str(try_global))
    elif try_global == "" and message.find(key2) != -1:
        message = message.replace(key2, "")
    
    if try_tr != "" and message.find(key3) != -1:
        message = message.replace(key3, str(try_tr))
    elif try_tr == "" and message.find(key3) != -1:
        message = message.replace(key3, "")
    
    return message


def send_push_notifications(message):
    if config.TEST:
        print("TEST:", message)
    else:
        print("Sending notification...")
        appobj = apprise.Apprise()
        for key, value in config.NOTIFICATIONS.items():
            endpoint = ""
            if key == "DISCORD":
                for wid, wtk in value.items():
                    if wid != "message": endpoint = f"discord://{wid}/{wtk}?avatar_url={config.NOTIFICATIONS['avatarURL']}"
                message += "\n" + value["message"]
            elif key == "TELEGRAM":
                for tkn, cid in value.items():
                    endpoint = f'tgram://{tkn}'
                    for c in cid:
                        endpoint += f'/{c}'
            else:
                continue
            
            isokay = appobj.add(endpoint)
            if config.DEBUG: print(f"{key}: {endpoint} is okay: {isokay}")
            
        if config.DEBUG: print("Loaded notification count: " + len(appobj).__str__())
        
        appobj.notify(body=message, title="""Binance Arbitage USDT/TRY - TRY/USDT""") # """notify_type=apprise.NotifyType.SUCCESS"""
        
        if config.DEBUG_HTTP: print(appobj.details())
        print(message)
        
        appobj.clear()


print("Starting...")
# make a timer for run every 1 minute
while (True):
    try_global = get_binance_global_fiat_buy_usdt()
    try_tr = get_binance_tr_last_sell_usdt()
    message = message_parser(try_global, try_tr, "")
    
    cond1 = (config.LAST_GLOBAL_TRY != try_global or config.LAST_TR_TRY != try_tr)
    cond2 = (config.LAST_GLOBAL_TRY == 0.0 and config.LAST_TR_TRY == 0.0)
    cond3 = (try_tr - try_global) >= 1.0
    
    if (cond2 or cond1) and cond3:
        config.LAST_GLOBAL_TRY = try_global
        config.LAST_TR_TRY = try_tr
        send_push_notifications(message)
    else:
        print("No notification sent.\n" + message)
    time.sleep(60)
    
