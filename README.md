# Screw Top Lid - Remix

This is a set of measured and tested parametric models of replacement jar lids for Anko glass jars, available from KMart in Australia. The original model was done by Steve De Groof (@SteveDeGroof), downloaded from  https://www.printables.com/model/1798563-parametric-screw-top-lid in August 2026.

Over time, the original metal jar lids get rusty and generally yucky, so a printable replacement is a good idea. Note that we don't use the seal - we rely on the plastic to form a "good enough" seal on the top of the glass. This is probably not enough for pickling or long term food storage, but for dry spices or small items it's perfectly good I think.

Note that the 120mL jar has had (at least) two versions - I've designated these as the "old" version, and the "new" version. The "new" version is the one currently on sale, I believe. I don't know when the changeover happened, but I have a whole bunch of the old jars in use.

## Generate lids from CSV

Edit `parameters.csv`, adding one row per lid. The first column, `name`, is the output filename (the `.scad` extension is optional). The remaining columns are the numeric parameters from the top of `jar_lids.scad`:

| Column | Parameter                                |
| ------ | ---------------------------------------- |
| d      | Container neck diameter                  |
| p      | Thread pitch                             |
| h      | Thread height                            |
| w      | Thread width                             |
| tr     | Thread turns                             |
| nt     | Number of threads                        |
| cd     | Inner cap depth                          |
| ts     | Thread start distance from bottom of cap |
| th     | Cap thickness                            |
| rdg    | Number of ridges                         |
| cl     | Clearance                                |

Run with Python 3.9 or newer; no extra packages are needed:

```sh
python3 generate_lids.py
```

This creates `generated/jar_lids-default.scad` from the sample row. Each row
must supply every parameter. Only assignments above the Customizer boundary
are replaced; comments, calculated values and model geometry are preserved.
Rerunning the script replaces existing generated files with matching names.
The master template is protected against overwriting.

To choose another CSV, master file or output directory:

```sh
python3 generate_lids.py my_lids.csv --template jar_lids.scad --output-dir output
```
