TEST = False
DEBUG = False
DEBUG_HTTP = False

NOTIFICATIONS = {
    "DISCORD": {
        # https://discord.com/api/webhooks/{WebhookID}/{WebhookToken}
        # WebhookID: WebhookToken
        "1109723951548168": "jUOJNIexDsctiur-klyOxhnG3jJHHsbjsOJCkY1Z0DF0DoblXQQ3yyAdUiRXkfhGITq",
        "message": "@everyone",
    },
    "TELEGRAM": {
        # token: [chat_id1, chat_id2, ...]
        "1763253434:AACAdrgA6BX-OKBt0v7Q0NsjkNOSd4bfsqLG4": ["915635438"],
    },
    
    "avatarURL": "https://upload.wikimedia.org/wikipedia/commons/5/57/Binance_Logo.png"
}

BINANCE_GLOBAL_BUY_CRYPTO_WITH_FIAT_API = "https://www.binance.com/bapi/fiat/v3/public/fiatpayment/buy/get-crypto-list?fiatCurrency=TRY"
BINANCE_TR_LAST_SELL_USDT_API = "https://www.trbinance.com/open/v1/market/agg-trades?symbol=USDT_TRY&limit=1"

MESSAGE_TEMPLATE = """
%date%
Binance Global 1 USDT ≈ %TRY_GLOBAL% TRY.
Binance TR 1 USDT ≈ %TRY_TR% TRY.
%message%"""

LAST_GLOBAL_TRY = 0.0
LAST_TR_TRY = 0.0