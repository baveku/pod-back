import sys

import win32com.client

args = sys.argv[1:]
PSD_PATH = args[0]
ORDER_IDS = args[1].split(',')
TEXT_INPUTS = args[2].split(',')

ps = win32com.client.Dispatch("Photoshop.Application")

doc = ps.Open(PSD_PATH)
doc.Close()
sys.stdout.flush()