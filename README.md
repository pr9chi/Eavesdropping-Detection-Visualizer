# ⚛️ BB84 Quantum Key Distribution Simulator
Cirq + qsim + Streamlit Interactive Visualizer

An interactive, simulation-based educational tool that demonstrates how the BB84 quantum key distribution protocol detects eavesdropping using the laws of quantum mechanics.
Built with Python, Streamlit, Cirq, and qsim, this visualizer models secure communication between Alice and Bob and shows how an eavesdropper (Eve) introduces detectable  errors due to quantum measurement disturbance.

# ✨ Features
- Toggle Eve on/off
- Qubit grid (match/error/discard)
- Sifted keys for Alice & Bob
- QBER meter (secure vs abort at 11%)
- No-Eve vs With-Eve comparison
- qsim fallback to Cirq

# 🧠 Concepts Covered
- BB84 Protocol
- Quantum superposition and measurement
- Basis selection (Z: |0⟩, |1⟩ and X: |+⟩, |−⟩)
- Sifted key generation
- Quantum Bit Error Rate (QBER)
- Eavesdropping detection via disturbance
- Circuit simulation using Cirq/qsim
