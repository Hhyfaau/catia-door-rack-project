import os
import win32com.client
import pythoncom
from pycatia import catia

WORK = r"C:\Users\Administrator\Documents\Codex\2026-08-30\zhao\work\rack_parts"
pythoncom.CoInitialize()
app = win32com.client.GetActiveObject("CATIA.Application")
app.DisplayFileAlerts = False
cat = catia()
for i in range(app.Documents.Count, 0, -1):
    try:
        app.Documents.Item(i).Close()
    except Exception:
        pass

L = 2400
HALF = 500
ZTOP = 780
ZBOT = 20
STEP = 240

beam920 = os.path.join(WORK, "Beam920.CATPart")
rail2360 = os.path.join(WORK, "Rail2360.CATPart")
post720 = os.path.join(WORK, "Post720.CATPart")
corner840 = os.path.join(WORK, "Corner840.CATPart")
v600 = os.path.join(WORK, "VBeam600.CATPart")

RX = (0, 0, -1, 0, 1, 0, 1, 0, 0)   # local Z->world X
RY = (-1, 0, 0, 0, 0, 1, 0, 1, 0)   # local Z->world Y, local Y->world +Z
RZ = (1, 0, 0, 0, 1, 0, 0, 0, 1)

# (file, R, tx, ty, tz)
members = []
# top beams (11) beam along +Y, start y=-460, span -460..+460
for i in range(11):
    members.append((beam920, RY, i * STEP, -460, ZTOP))
# top rail (1) at Y=-480 (non-post side), along +X from x=20
members.append((rail2360, RX, 20, -HALF + 20, ZTOP))
# bottom long rails (2) Y=+-480
for y in (-HALF + 20, HALF - 20):
    members.append((rail2360, RX, 20, y, ZBOT))
# bottom inner beams (2) Y=+-120
for y in (-120, 120):
    members.append((rail2360, RX, 20, y, ZBOT))
# bottom end rails (2) X=0,L, beam along +Y
for x in (0, L):
    members.append((beam920, RY, x, -460, ZBOT))
# normal posts (9) at Y=+480 (post side), X=240..2160, vertical +Z
for i in range(1, 10):
    members.append((post720, RZ, i * STEP, HALF - 20, 40))
# corner posts (4) with handles, X in {0,L}, Y in {-480,+480}
for x in (0, L):
    for y in (-HALF + 20, HALF - 20):
        members.append((corner840, RZ, x, y, 40))
# V beams (10) opening up, on bottom frame (vertex z=40, opening z=70)
for i in range(10):
    members.append((v600, RY, (i + 0.5) * STEP, -300, 70))

files = tuple(m[0] for m in members)
prod = app.Documents.Add("Product")
pd = cat.active_document
root = pd.product
root.products.add_components_from_files(files, "CATPart")
comps = list(root.products)
print("components:", len(comps), "expected:", len(members))
for comp, m in zip(comps, members):
    file, R, tx, ty, tz = m
    comp.position.set_components((*R, tx, ty, tz))
root.update()
out = os.path.join(WORK, "DoorRack3.CATProduct")
pd.save_as(out, overwrite=True)
print("saved", out)
