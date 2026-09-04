import os
import win32com.client
import pythoncom
from pycatia import catia

WORK = r"C:\Users\Administrator\Documents\Codex\2026-08-30\zhao\work\rack_parts"
OUT = r"C:\Users\Administrator\Documents\Codex\2026-08-30\zhao\outputs\step"

pythoncom.CoInitialize()
app = win32com.client.GetActiveObject("CATIA.Application")
app.DisplayFileAlerts = False
cat = catia()

for i in range(app.Documents.Count, 0, -1):
    try:
        app.Documents.Item(i).Close()
    except Exception:
        pass

app.Documents.Open(os.path.join(WORK, "DoorRack3.CATProduct"))
pd = cat.active_document
os.makedirs(OUT, exist_ok=True)
out = os.path.join(OUT, "DoorRack3_assembly.stp")
pd.export_data(out, "stp", overwrite=True)
print("exported:", out, os.path.exists(out), os.path.getsize(out))
