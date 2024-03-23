SAVE_LOGS = False

# RANDOM WALLETS MODE
RANDOM_WALLET = True  # True/False

USE_PROXY = True

SLEEP_FROM = 1500  # Second
SLEEP_TO = 3600  # Second

QUANTITY_THREADS = 50

THREAD_SLEEP_FROM = 4000
THREAD_SLEEP_TO = 8000

# GWEI CONTROL MODE
CHECK_GWEI = True  # True/False
MAX_GWEI = 20
REALTIME_GWEI = True  # if true - you can change gwei while program is working

# Рандомизация гвея. Если включен режим, то максимальный гвей будет выбираться из диапазона
RANDOMIZE_GWEI = True  # if True, max Gwei will be randomized for each wallet for each transaction
MAX_GWEI_RANGE = [15, 18]

GAS_SLEEP_FROM = 70
GAS_SLEEP_TO = 180

GAS_MULTIPLIER = 1.1

# RETRY MODE
RETRY_COUNT = 3

LAYERSWAP_API_KEY = ""
