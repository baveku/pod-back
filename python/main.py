import os
import sys
from pathlib import Path

import win32com.client

args = sys.argv[1:]
PSD_PATH = args[0]
ORDER_IDS = args[1].split(',')
TEXT_INPUTS = args[2].split(',')
SKU = args[3]

OUTPUT_DIR = Path.joinpath(Path(PSD_PATH).parent.parent, 'POD-BACK')
os.makedirs(OUTPUT_DIR, exist_ok=True)
SKU_FOLDER_DIR = Path.joinpath(OUTPUT_DIR, SKU)
os.makedirs(SKU_FOLDER_DIR, exist_ok=True)

psApp = win32com.client.Dispatch("Photoshop.Application")
doc = psApp.Open(PSD_PATH)
layers = psApp.Application.ActiveDocument

for idx, val in enumerate(ORDER_IDS):
	file_export_name = ORDER_IDS[idx]
	replace_text = TEXT_INPUTS[idx]
	isMultiContent = len(replace_text.split('|')) > 1
	try:
		if isMultiContent == False:
			quote_layer = layers.ArtLayers["USER_CONTENT_NAME"]
			quote_layer.TextItem.contents = replace_text.strip()
		else:
			texts = replace_text.split('|')
			for ind, text in enumerate(texts):
				quote_layer = layers.ArtLayers["USER_CONTENT_NAME_{ind}".format(ind=ind)]
				quote_layer.TextItem.contents = replace_text.strip()
	except:
		print("An exception occurred")

	options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
	options.Format = 8
	options.Quality = 100
	fileName = file_export_name + "-" + replace_text + ".png"
	ourDir = SKU_FOLDER_DIR
	fileExport = Path.joinpath(ourDir, fileName)
	layers.Export(ExportIn=fileExport, ExportAs=2, Options=options)
doc.Close(2)
sys.stdout.flush()