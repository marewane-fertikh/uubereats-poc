import time

# Couleurs ANSI
RESET = "\033[0m"
BOLD = "\033[1m"

COL_CLIENT     = "\033[96m"   # cyan
COL_PLATEFORME = "\033[95m"   # magenta
COL_RESTAURANT = "\033[93m"   # jaune
COL_LIVREUR    = "\033[92m"   # vert
COL_ERROR      = "\033[91m"   # rouge

def timestamp():
    return time.strftime("%H:%M:%S")

def log(role_color, role, message):
    print(f"{role_color}[{timestamp()}] {role:<12}{RESET} | {message}")

def log_client(msg):     log(COL_CLIENT,     "CLIENT",     msg)
def log_plateforme(msg): log(COL_PLATEFORME, "PLATEFORME", msg)
def log_restaurant(msg): log(COL_RESTAURANT, "RESTAURANT", msg)
def log_livreur(lid, msg): log(COL_LIVREUR, f"LIVREUR {lid}", msg)
def log_error(msg):      log(COL_ERROR,      "ERROR",      msg)
