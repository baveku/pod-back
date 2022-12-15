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
psApp.Open(PSD_PATH)
layers = psApp.Application.ActiveDocument

for idx, val in enumerate(ORDER_IDS):
	file_export_name = ORDER_IDS[idx]
	replace_text = TEXT_INPUTS[idx]
	quote_layer = layers.ArtLayers["USER_CONTENT_NAME"]
	quote_layer.TextItem.contents = replace_text.strip()

	options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
	options.Format = 8
	options.Quality = 100
	
	fileName=(Path.joinpath(OUTPUT_DIR, file_export_name + "-" + replace_text + ".png"))
	layers.Export(ExportIn=fileName, ExportAs=2, Options=options)

while psApp.Documents.Count > 0:
    psApp.ActiveDocument.Close(2)
sys.stdout.flush()