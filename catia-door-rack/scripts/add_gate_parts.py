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
gateset = {"UBeam540.CATPart", "GatePost.CATPart"}
rm = [i for i, c in enumerate(comps)
      if c.reference_product.file_name in gateset]
print("removing existing gate parts:", len(rm))
for i in sorted(rm, reverse=True):
    try:
        root.products.remove(i + 1)
    except Exception:
        pass

# gate posts at local X=20 and 520 (500 apart) -> align with connectors 700/1200/1700/2200
ubeam = os.path.join(WORK, "UBeam540.CATPart")
post = os.path.join(WORK, "GatePost.CATPart")
beams = [-480, -120, 120, 420]
gate_pos = [680, 1680]   # -> posts at (700,1200) and (1700,2200)
items = []
for by in beams:
    for gp in gate_pos:
        items.append((ubeam, gp, by, -153))
        items.append((post, gp + 20, by, -150))
        items.append((post, gp + 520, by, -150))
root.products.add_components_from_files(tuple(i[0] for i in items), "CATPart")
new = list(root.products)[-len(items):]
RZ = (1, 0, 0, 0, 1, 0, 0, 0, 1)
for c, (_, x, y, z) in zip(new, items):
    c.position.set_components((*RZ, x, y, z))
root.update()
cat.active_document.save_as(os.path.join(WORK, "DoorRack3.CATProduct"), overwrite=True)
print("placed gate parts; posts at X = 700/1200/1700/2200; total comps:", len(list(root.products)))
