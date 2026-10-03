#!/usr/bin/env python3
"""Rebuild the download ZIPs for the R.A.M.P.A.T. site.

Run from the repo root:  python3 tools/build_zips.py

Inputs
  source/cad/RAMPAT-full-assembly.step   full Onshape assembly
  source/cad/parts-list.csv              part index for the STL pack
  files/cad/stl/<group>/*.stl            individual printable parts
  source/pcb/*                           Gerber + drill files from KiCad
  files/RAMPAT-poster-2026.pdf           project poster

Outputs
  files/cad/RAMPAT-CAD-assembly-STEP.zip
  files/cad/RAMPAT-printable-STL.zip
  files/pcb/RAMPAT-PCB.zip
  files/RAMPAT-all-files.zip
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, FILES = ROOT / "source", ROOT / "files"
Z = dict(compression=zipfile.ZIP_DEFLATED, compresslevel=9)

STEP_README = """R.A.M.P.A.T. full assembly (STEP AP214, millimetres)

Open in Onshape, Fusion, SolidWorks or FreeCAD to modify the design.
The assembly includes purchased hardware (motors, servos, screws, carbon tubes)
for reference. Only the parts in the STL pack need printing.

License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
"""

STL_README = """R.A.M.P.A.T. printable parts (STL, millimetres)

One file per physical part. Left (L) and right (R) parts are mirrored,
so print each file once. parts-list.csv maps each file to its Onshape name.
Material: LW-PETG, gyroid infill.
  Fuselage shells (nose cone, front, center): 1 wall loop, 3% infill
  Wings (wing panels, ailerons):              1 wall loop, 5% infill
  Connectors (joiners, mounts, root plates):  3 wall loops, 20% infill
  Everything else:                            2 wall loops, 20% infill
The print_profile column in parts-list.csv gives the profile for each file.
Orient parts in your slicer before printing.

License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
"""

ALL_README = """R.A.M.P.A.T. complete file set

CAD/STEP   full assembly for modification
CAD/STL    individual parts for printing
PCB        flight controller Gerber ZIP; upload it unchanged to your PCB fab
           (4 layers, 1.6 mm, HASL)

License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
"""


def add_tree(zf, folder, arc_prefix):
    for f in sorted(Path(folder).rglob("*")):
        if f.is_file():
            zf.write(f, f"{arc_prefix}/{f.relative_to(folder).as_posix()}")


def build():
    step = SRC / "cad" / "RAMPAT-full-assembly.step"
    stl_dir = FILES / "cad" / "stl"
    parts_csv = SRC / "cad" / "parts-list.csv"
    pcb_dir = SRC / "pcb"
    poster = FILES / "RAMPAT-poster-2026.pdf"

    out = FILES / "cad" / "RAMPAT-CAD-assembly-STEP.zip"
    with zipfile.ZipFile(out, "w", **Z) as z:
        z.write(step, "RAMPAT-full-assembly.step")
        z.writestr("README.txt", STEP_README)
    print("built", out.relative_to(ROOT))

    out = FILES / "cad" / "RAMPAT-printable-STL.zip"
    with zipfile.ZipFile(out, "w", **Z) as z:
        add_tree(z, stl_dir, "stl")
        z.write(parts_csv, "parts-list.csv")
        z.writestr("README.txt", STL_README)
    print("built", out.relative_to(ROOT))

    out = FILES / "pcb" / "RAMPAT-PCB.zip"
    with zipfile.ZipFile(out, "w", **Z) as z:
        # files at the ZIP root, so it can be uploaded straight to a PCB fab
        for f in sorted(pcb_dir.iterdir()):
            if f.is_file():
                z.write(f, f.name)
    print("built", out.relative_to(ROOT))

    out = FILES / "RAMPAT-all-files.zip"
    with zipfile.ZipFile(out, "w", **Z) as z:
        z.write(step, "CAD/STEP/RAMPAT-full-assembly.step")
        add_tree(z, stl_dir, "CAD/STL")
        z.write(parts_csv, "CAD/STL/parts-list.csv")
        z.write(FILES / "pcb" / "RAMPAT-PCB.zip", "PCB/RAMPAT-FC-gerbers.zip")
        if (ROOT / "LICENSE.txt").exists():
            z.write(ROOT / "LICENSE.txt", "LICENSE.txt")
        if poster.exists():
            z.write(poster, "RAMPAT-poster-2026.pdf")
        z.writestr("README.txt", ALL_README)
    print("built", out.relative_to(ROOT))

    for p in sorted(FILES.rglob("*.zip")):
        mb = p.stat().st_size / 1e6
        warn = "  <-- over GitHub's 100 MB limit" if mb > 100 else ""
        print(f"  {p.relative_to(ROOT)}  {mb:.1f} MB{warn}")


if __name__ == "__main__":
    build()
