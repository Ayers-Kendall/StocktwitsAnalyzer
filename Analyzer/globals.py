

# ----------------- Define global counters ------------------- #
alpha_vantage_api_call_count = 0
iex_api_call_count = 0

# ------------------------------------------------------------ #


# ----------------- Define all constants ------------------- #
INCREASING_COLOR = '#00BB00'
DECREASING_COLOR = '#BB0000'

ALPHA_VANTAGE_API_KEYS = []
IEX_SECRET_KEYS = []
WTC_API_KEYS = []
INTRINIO_API_KEYS = []
with open("../API_keys/AlphaVantage_API_keys", "r") as file:
    for line in file.readlines():
        try:
            key = (line[0 : line.index('#')]).trim()
        except:
            key = line.trim()
        ALPHA_VANTAGE_API_KEYS.append(key)
    
    file = open("../API_keys/WorldTradingData_API_keys", "r")
    for line in file.readlines():
        try:
            key = (line[0 : line.index('#')]).trim()
        except:
            key = line.trim()
        IEX_SECRET_KEYS.append(key)
    
    file = open("../API_keys/IEX_API_keys", "r")
    for line in file.readlines():
        try:
            key = (line[0 : line.index('#')]).trim()
        except:
            key = line.trim()
        WTC_API_KEYS.append(key)
    
    file = open("../API_keys/Intrinio_API_keys", "r")
    for line in file.readlines():
        try:
            key = (line[0 : line.index('#')]).trim()
        except:
            key = line.trim()
        INTRINIO_API_KEYS.append(key)

# ---------------------------------------------------------- #
