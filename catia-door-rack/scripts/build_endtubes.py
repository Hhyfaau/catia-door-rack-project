import os
import win32com.client
import pythoncom
from pycatia import catia

WORK = r"C:\Users\Administrator\Documents\Codex\2026-08-30\zhao\work\rack_parts"
pythoncom.CoInitialize()
app = win32com.client.GetActiveObject("CATIA.Application")
app.DisplayFileAlerts = False
cat = catia()

# close stray part docs so files can be written
for i in range(app.Documents.Count, 0, -1):
    if app.Documents.Item(i).Name.lower().endswith(".catpart"):
        try:
            app.Documents.Item(i).Close()
        except Exception:
            pass


def pline(f2, pts):
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        f2.create_line(x1, y1, x2, y2)


# rectangular box tube: cross 40(Y) x 153(Z), length 500 along X, wall 3
pd = app.Documents.Add("Part")
p = cat.active_document
part = p.part
body = part.bodies.item(1)
plane_yz = part.origin_elements.plane_yz
sk = body.sketches.add(plane_yz)
f2 = sk.open_edition()
# outer rectangle (y,z): width 40 -> y -20..20 ; height 153 -> z -76.5..76.5
pline(f2, [(-20, -76.5), (20, -76.5), (20, 76.5), (-20, 76.5)])
sk.close_edition()
part.in_work_object = sk
part.shape_factory.add_new_pad(sk, 250)
sk2 = body.sketches.add(plane_yz)
f2b = sk2.open_edition()
pline(f2b, [(-17, -73.5), (17, -73.5), (17, 73.5), (-17, 73.5)])
sk2.close_edition()
part.in_work_object = sk2
pkt = part.shape_factory.add_new_pocket(sk2, 250)
pkt.first_limit.limit_mode = 2
part.update()
path = os.path.join(WORK, "EndTube250.CATPart")
p.save_as(path, overwrite=True)
app.Documents.Item(app.Documents.Count).Close()
print("saved", path)
