# QCXMS

**QCXMS** is a lightweight Python wrapper around the `qcxms` quantum chemistry code. It simplifies the setup, execution, and interpretation of quantum chemical mass spectrometry simulations. With a single `.mol` file, users can easily simulate CID spectra, visualize the results, and assign specific fragments to their corresponding m/z peaks.

---

## ✨ Features

- 🔬 **One-command MS simulation** from `.mol` files
- 📈 **Spectra plotting** with peak intensities and labels
- 🧩 **Fragment-to-peak assignment** – instantly see which structures correspond to each peak
- 🗂️ **Output handling** – generates clean, readable output files
- 🧵 **Robust job management** – identifies and resubmits unfinished simulations

---

## 🚀 Quick Start

### 1. Prepare your molecule

Save your molecule as a `.mol` file. You can easily do this using tools like [ChemDraw](https://www.perkinelmer.com/category/chemdraw) or [Avogadro](https://avogadro.cc/).

Example: `succinic_acid.mol`

---

### 2. Run a simulation

From your terminal:

```bash
cid succinic_acid 20 80 5
```
This simulates CID spectra for succinic_acid.mol with collision energies from 20 eV to 80 eV in 5 eV steps.

To simulate a single energy:
```bash
cid succinic_acid 40
```

3. Plot the MS spectrum
```bash
plotms
```

This generates:

An annotated MS spectrum

Tabulated m/z values and intensities

A report of any missing or unfinished simulations

4. View structures responsible for a peak
```bash
structure
```

This first displays:

m/z     Intensity

45.0    0.78

61.0    0.54
...

Then, to fetch the structures contributing to a given peak:

```bash
structure 61.0
```

All generated fragment structures contributing to m/z = 61.0 will be shown or visualized.

## 📁 Output Files

- `*.txt` – machine- and human-readable summaries
- `*.png` – spectrum plots
- `structures/` – folder with fragment structures organized by peak

---

## 📦 Installation & Requirements

This tool assumes `qcxms` is properly installed and available in your `PATH`. Python 3.x with `matplotlib` and `pandas` is also required.


## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🙌 Acknowledgments

This wrapper is built around the [QCxMS](https://www.chemie.uni-bonn.de/pctc/mulliken-center/software/qcxms/qcxms) code developed by the University of Bonn. It aims to make high-level mass spectrometry simulations more accessible for chemists and cheminformaticians alike.

---

## 🧪 Example

![Example Spectrum](example_spectrum.png)

---

## 🧠 Citation

If you use this tool in your work, please consider citing the original QCxMS paper:

> Grimme, S. et al. _QCxMS – A Program for Calculating Collision-Induced Dissociation Mass Spectra._ J. Chem. Theory Comput. 2020.

---

Happy simulating!
