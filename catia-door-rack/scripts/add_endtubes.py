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
# remove old EndTube500 instances
rm = [i for i, c in enumerate(comps)
      if c.reference_product.file_name == "EndTube500.CATPart"]
for i in sorted(rm, reverse=True):
    try:
        root.products.remove(i + 1)
    except Exception:
        pass
print("removed old end tubes:", len(rm))

tube = os.path.join(WORK, "EndTube250.CATPart")
items = [
    (tube, 20, 120, -76.5),
    (tube, 20, -120, -76.5),
]
root.products.add_components_from_files(tuple(i[0] for i in items), "CATPart")
new = list(root.products)[-len(items):]
RZ = (1, 0, 0, 0, 1, 0, 0, 0, 1)
for c, (_, x, y, z) in zip(new, items):
    c.position.set_components((*RZ, x, y, z))
root.update()
cat.active_document.save_as(os.path.join(WORK, "DoorRack3.CATProduct"), overwrite=True)
print("placed 2 tubes at X=20..270, Y=+-120 (center beams), Z=-153..0; total:", len(list(root.products)))
