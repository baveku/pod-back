import os
import sys
from pathlib import Path

import win32com.client

args = sys.argv[1:]
PSD_PATH = args[0]
ORDER_IDS = args[1].split(',')
TEXT_INPUTS = args[2].split(',')

OUTPUT_DIR = Path.joinpath(Path(PSD_PATH).parent.parent, 'POD-BACK')
os.makedirs(OUTPUT_DIR, exist_ok=True)

psApp = win32com.client.Dispatch("Photoshop.Application")
doc = psApp.Open(PSD_PATH)
layers = psApp.Application.ActiveDocument

for idx, val in enumerate(ORDER_IDS):
	file_export_name = ORDER_IDS[idx]
	replace_text = TEXT_INPUTS[idx]
	try:
		quote_layer = layers.ArtLayers["USER_CONTENT_NAME"]
		quote_layer.TextItem.contents = replace_text.strip()
	except:
		print("An exception occurred")

	options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
	options.Format = 8
	options.Quality = 100
	canCreateFolder = ORDER_IDS.count(file_export_name) > 1
	fileName = file_export_name + "-" + replace_text + ".png"
	ourDir = OUTPUT_DIR
	if canCreateFolder:
		orderOutputDIR = Path.joinpath(OUTPUT_DIR, file_export_name)
		os.makedirs(orderOutputDIR, exist_ok=True)
		ourDir = orderOutputDIR
	fileExport = Path.joinpath(ourDir, fileName)
	layers.Export(ExportIn=fileExport, ExportAs=2, Options=options)
doc.Close(2)
sys.stdout.flush()