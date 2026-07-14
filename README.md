# ⚛️ BB84 Quantum Key Distribution Visualizer

An interactive Streamlit app that simulates the BB84 quantum key distribution protocol and visualizes how eavesdropping affects secure key generation.

The app shows Alice and Bob preparing and measuring qubits in randomly chosen bases, then compares sifted keys and computes the Quantum Bit Error Rate (QBER). When Eve is enabled, the simulation demonstrates how measurement disturbance introduces detectable errors.

## ✨ Features
- Interactive toggle for an eavesdropper (Eve)
- Visual qubit grid showing matches, errors, and discarded qubits
- Sifted key display for Alice and Bob
- QBER meter with a secure/abort threshold
- Side-by-side comparison of no-Eve and with-Eve behavior
- Uses `qsimcirq` when available, otherwise falls back to Cirq simulator

## 🚀 Requirements
- Python 3.10+
- `streamlit`
- `cirq`
- `numpy`
- Optional: `qsimcirq` for faster simulation

## 📦 Installation
1. Create and activate a Python virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install streamlit cirq numpy
```

3. (Optional) Install `qsimcirq` for improved performance:

```powershell
pip install qsimcirq
```

## ▶️ Run the app

From the project directory:

```powershell
streamlit run Eavesdropping-Detection-Visualizer.py
```

## 🧠 What it demonstrates
- BB84 basis selection using Z and X bases
- Quantum state preparation and measurement
- How Eve's measurement disturbs qubits
- Sifted key agreement between Alice and Bob
- Quantum Bit Error Rate (QBER) and eavesdropping detection threshold

## 📁 Project files
- `Eavesdropping-Detection-Visualizer.py` — Streamlit app and BB84 simulation logic
- `README.md` — Project overview and run instructions

## 💡 Notes
- The app is intended as an educational visualizer, not a production cryptography system.
- If `qsimcirq` is not installed, the project will still run using the default Cirq simulator.
