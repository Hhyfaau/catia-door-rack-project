import os
import win32com.client
import pythoncom
from pycatia import catia

WORK = r"C:\Users\Administrator\Documents\Codex\2026-08-30\zhao\work\rack_parts"
pythoncom.CoInitialize()
app = win32com.client.GetActiveObject("CATIA.Application")
app.DisplayFileAlerts = False
cat = catia()

app.Documents.Open(os.path.join(WORK, "DoorRack3.CATProduct"))
root = cat.active_document.product
comps = list(root.products)
beams = [-480, -120, 120, 420]
pxs = [200, 1250]
RZ = (1, 0, 0, 0, 1, 0, 0, 0, 1)
idx = 0
for c in comps:
    try:
        fn = c.reference_product.file_name
    except Exception:
        fn = "ERR"
    if fn == "ERR":          # the 8 gate sub-assemblies
        by = beams[idx // 2]
        px = pxs[idx % 2]
        c.position.set_components((*RZ, px, by, -153))   # post top (local 153) -> world 0
        idx += 1
root.update()
cat.active_document.save_as(os.path.join(WORK, "DoorRack3.CATProduct"), overwrite=True)
print("positioned", idx, "gates at Z=-153 (post top=0)")
