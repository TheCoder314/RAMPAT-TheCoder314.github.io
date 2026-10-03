# R.A.M.P.A.T.

**Rapid, Affordable, Modular, Printed, Aerial Tiltrotor** — an open-source, 3D-printed tiltrotor VTOL for emergency response, by Aarit Dixit.

Website: `https://thecoder314.github.io/RAMPAT-TheCoder314.github.io/`

## Downloads

| File | Contents |
| --- | --- |
| `files/RAMPAT-all-files.zip` | Everything: STEP, STLs, PCB Gerbers, poster |
| `files/cad/RAMPAT-CAD-assembly-STEP.zip` | Full assembly for modification |
| `files/cad/RAMPAT-printable-STL.zip` | 53 printable parts + parts list |
| `files/pcb/RAMPAT-PCB.zip` | Flight controller Gerbers, upload directly to a fab |

## Printing (LW-PETG, gyroid infill)

| Parts | Walls | Infill |
| --- | --- | --- |
| Fuselage shells | 1 | 3% |
| Wings | 1 | 5% |
| Connectors | 3 | 20% |
| Everything else | 2 | 20% |

## Repo layout

```
index.html              the website
assets/                 images and part thumbnails
files/                  everything visitors download
source/cad/             full STEP assembly + parts-list.csv
source/pcb/             Gerber + drill files from KiCad
tools/build_zips.py     rebuilds every ZIP in files/
```

After changing anything in `source/` or `files/cad/stl/`, run `python3 tools/build_zips.py`.

## Publish on GitHub Pages

1. Push this folder to a GitHub repository.
2. Settings → Pages → Deploy from a branch → `main`, `/ (root)`.

## License

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). See `LICENSE.txt`.
