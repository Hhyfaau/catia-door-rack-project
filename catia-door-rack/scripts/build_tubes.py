import os
import win32com.client
import pythoncom
from pycatia import catia

WORK = r"C:\Users\Administrator\Documents\Codex\2026-08-30\zhao\work\rack_parts"
os.makedirs(WORK, exist_ok=True)
pythoncom.CoInitialize()
app = win32com.client.GetActiveObject("CATIA.Application")
app.DisplayFileAlerts = False
cat = catia()

for i in range(app.Documents.Count, 0, -1):
    try:
        app.Documents.Item(i).Close()
    except Exception:
        pass


def rect(f2, h):
    f2.create_line(-h, -h, h, -h)
    f2.create_line(h, -h, h, h)
    f2.create_line(h, h, -h, h)
    f2.create_line(-h, h, -h, -h)


def tube(name, length, outer=40, wall=2.5):
    pd = cat.documents.add("Part")
    p = cat.active_document
    part = p.part
    body = part.bodies.item(1)
    plane = part.origin_elements.plane_xy
    sk = body.sketches.add(plane)
    f2 = sk.open_edition()
    rect(f2, outer / 2)
    sk.close_edition()
    part.in_work_object = sk
    part.shape_factory.add_new_pad(sk, length)
    sk2 = body.sketches.add(plane)
    f2b = sk2.open_edition()
    rect(f2b, (outer - 2 * wall) / 2)
    sk2.close_edition()
    part.in_work_object = sk2
    pkt = part.shape_factory.add_new_pocket(sk2, length)
    pkt.first_limit.limit_mode = 2
    part.update()
    path = os.path.join(WORK, name + ".CATPart")
    p.save_as(path, overwrite=True)
    return path


def vbeam(name, length=600, hw=22, depth=30, vt=4):
    pd = cat.documents.add("Part")
    p = cat.active_document
    part = p.part
    body = part.bodies.item(1)
    plane = part.origin_elements.plane_xy
    sk = body.sketches.add(plane)
    f2 = sk.open_edition()
    pts = [(-hw, 0), (0, -depth), (hw, 0), (hw - vt, 0), (0, -depth + vt), (-hw + vt, 0)]
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        f2.create_line(x1, y1, x2, y2)
    sk.close_edition()
    part.in_work_object = sk
    part.shape_factory.add_new_pad(sk, length)
    part.update()
    path = os.path.join(WORK, name + ".CATPart")
    p.save_as(path, overwrite=True)
    return path


beam920 = tube("Beam920", 920)
rail2360 = tube("Rail2360", 2360)
post720 = tube("Post720", 720)
corner840 = tube("Corner840", 840)
v600 = vbeam("VBeam600")
print("templates:")
for x in (beam920, rail2360, post720, corner840, v600):
    print(" ", x)
