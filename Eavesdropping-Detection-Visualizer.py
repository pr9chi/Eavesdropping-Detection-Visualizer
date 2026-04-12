import streamlit as st
import random
import numpy as np
import time

# ── Quantum imports ──────────────────────────────────────────────────────────
import cirq
try:
    import qsimcirq
    _SIMULATOR = qsimcirq.QSimSimulator()          
    _SIM_LABEL = "qsim"
except ImportError:
    _SIMULATOR = cirq.Simulator()                  
    _SIM_LABEL = "cirq (qsim not found)"

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BB84 Quantum Key Distribution",
    page_icon="⚛️",
    layout="wide",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');
:root {
    --bg:#050a14;--surface:#0b1628;--card:#0d1f38;
    --accent1:#00e5ff;--accent2:#7b2fff;--accent3:#ff2d78;
    --green:#00ff9d;--yellow:#ffe600;--text:#c8e0ff;--muted:#4a6fa0;
    --font-mono:'Share Tech Mono',monospace;
    --font-head:'Orbitron',sans-serif;
    --font-body:'Exo 2',sans-serif;
}
html,body,[class*="css"]{background-color:var(--bg)!important;color:var(--text)!important;font-family:var(--font-body);}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:1.5rem;max-width:1400px;}
.hero{text-align:center;padding:2.5rem 1rem 1.5rem;}
.hero h1{font-family:var(--font-head);font-size:clamp(1.6rem,4vw,3.2rem);font-weight:900;letter-spacing:.12em;
  background:linear-gradient(90deg,var(--accent1),var(--accent2),var(--accent3));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:.3rem;}
.hero sub{font-family:var(--font-mono);font-size:.85rem;color:var(--muted);letter-spacing:.2em;}
.q-card{background:var(--card);border:1px solid rgba(0,229,255,.12);border-radius:12px;
  padding:1.4rem 1.6rem;margin-bottom:1rem;
  box-shadow:0 4px 32px rgba(0,0,0,.5),inset 0 1px 0 rgba(0,229,255,.06);}
.q-card h3{font-family:var(--font-head);font-size:.75rem;letter-spacing:.22em;color:var(--accent1);
  margin-bottom:.9rem;text-transform:uppercase;}
.metric-row{display:flex;gap:.7rem;flex-wrap:wrap;margin-bottom:.5rem;}
.metric-pill{background:rgba(0,229,255,.07);border:1px solid rgba(0,229,255,.18);border-radius:8px;
  padding:.45rem 1rem;flex:1;min-width:110px;text-align:center;}
.metric-pill .val{font-family:var(--font-mono);font-size:1.5rem;color:var(--accent1);line-height:1.1;}
.metric-pill .lbl{font-size:.65rem;letter-spacing:.15em;color:var(--muted);text-transform:uppercase;}
.badge{display:inline-block;font-family:var(--font-mono);font-size:.78rem;padding:.3rem .9rem;
  border-radius:20px;letter-spacing:.1em;font-weight:700;}
.badge-secure{background:rgba(0,255,157,.12);color:var(--green);border:1px solid var(--green);}
.badge-abort{background:rgba(255,45,120,.12);color:var(--accent3);border:1px solid var(--accent3);}
.qbit-grid{display:flex;flex-wrap:wrap;gap:5px;font-family:var(--font-mono);font-size:.7rem;}
.qbit{width:30px;height:30px;border-radius:6px;display:flex;align-items:center;justify-content:center;
  font-weight:700;transition:transform .15s;cursor:default;}
.qbit:hover{transform:scale(1.2);z-index:2;}
.qbit-match{background:rgba(0,255,157,.15);color:var(--green);border:1px solid rgba(0,255,157,.35);}
.qbit-err{background:rgba(255,45,120,.15);color:var(--accent3);border:1px solid rgba(255,45,120,.35);}
.qbit-discard{background:rgba(74,111,160,.10);color:var(--muted);border:1px solid rgba(74,111,160,.25);}
.channel{display:flex;align-items:center;gap:0;margin:.6rem 0;font-family:var(--font-mono);
  font-size:.72rem;overflow-x:auto;}
.node{padding:.5rem .9rem;border-radius:8px;white-space:nowrap;font-weight:700;letter-spacing:.05em;}
.node-alice{background:rgba(0,229,255,.12);color:var(--accent1);border:1px solid rgba(0,229,255,.3);}
.node-bob{background:rgba(0,255,157,.12);color:var(--green);border:1px solid rgba(0,255,157,.3);}
.node-eve{background:rgba(255,45,120,.12);color:var(--accent3);border:1px solid rgba(255,45,120,.3);}
.wire{flex:1;height:2px;min-width:18px;background:linear-gradient(90deg,var(--muted),var(--muted));position:relative;}
.wire::after{content:'▶';position:absolute;right:-6px;top:-9px;font-size:.8rem;color:var(--muted);}
.key-bits{display:flex;flex-wrap:wrap;gap:3px;font-family:var(--font-mono);font-size:.82rem;}
.kb{width:22px;height:22px;border-radius:4px;display:flex;align-items:center;justify-content:center;font-weight:700;}
.kb-0{background:rgba(0,229,255,.08);color:var(--accent1);border:1px solid rgba(0,229,255,.2);}
.kb-1{background:rgba(123,47,255,.18);color:#c4a0ff;border:1px solid rgba(123,47,255,.4);}
.kb-x{background:rgba(255,45,120,.08);color:var(--accent3);border:1px solid rgba(255,45,120,.25);}
.cmp-table{width:100%;border-collapse:collapse;font-family:var(--font-mono);font-size:.75rem;}
.cmp-table th{color:var(--muted);font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;
  padding:.4rem .6rem;border-bottom:1px solid rgba(255,255,255,.07);}
.cmp-table td{padding:.45rem .6rem;border-bottom:1px solid rgba(255,255,255,.04);}
.cmp-table tr:hover td{background:rgba(0,229,255,.03);}
.stButton>button{
  background:linear-gradient(135deg,#00e5ff22,#7b2fff22)!important;
  border:1px solid var(--accent2)!important;color:var(--accent1)!important;
  font-family:var(--font-head)!important;font-size:.72rem!important;letter-spacing:.18em!important;
  border-radius:8px!important;padding:.6rem 1.4rem!important;transition:all .2s!important;}
.stButton>button:hover{
  background:linear-gradient(135deg,#00e5ff44,#7b2fff44)!important;
  border-color:var(--accent1)!important;transform:translateY(-1px)!important;
  box-shadow:0 4px 20px rgba(0,229,255,.25)!important;}
section[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid rgba(0,229,255,.1);}
section[data-testid="stSidebar"] *{color:var(--text)!important;}
</style>
""", unsafe_allow_html=True)


# ─── Cirq + qsim quantum simulation ─────────────────────────────────────────
def _sample_probs(sv: np.ndarray) -> int:
    """Sample a 0/1 outcome from a 2-element statevector."""
    flat = sv.flatten()[:2]
    probs = np.abs(flat) ** 2
    probs /= probs.sum()
    return int(np.random.choice(2, p=probs))

def simulate_qubit_bb84(bit: int, alice_basis: str, bob_basis: str,
                         eve_basis: str | None) -> dict:
    q = cirq.LineQubit(0)
    eve_bit = None

    prep_ops = []
    if bit == 1:
        prep_ops.append(cirq.X(q))
    if alice_basis == "X":
        prep_ops.append(cirq.H(q))

    if eve_basis is not None:
        eve_ops = list(prep_ops)
        if eve_basis == "X":
            eve_ops.append(cirq.H(q))
        eve_ops.append(cirq.measure(q, key="eve"))

        eve_circuit = cirq.Circuit(eve_ops)
        eve_result = cirq.Simulator().run(eve_circuit, repetitions=1)
        eve_bit = int(eve_result.measurements["eve"][0][0])

        bob_ops = []
        if eve_bit == 1:
            bob_ops.append(cirq.X(q)) 
        if eve_basis == "X":
            bob_ops.append(cirq.H(q)) 
    else:
        bob_ops = list(prep_ops)

    if bob_basis == "X":
        bob_ops.append(cirq.H(q))
    bob_ops.append(cirq.measure(q, key="bob"))

    bob_circuit = cirq.Circuit(bob_ops)
    bob_result = _SIMULATOR.run(bob_circuit, repetitions=1) 
    bob_bit = int(bob_result.measurements["bob"][0][0])

    return {
        "alice_bit":   bit,
        "alice_basis": alice_basis,
        "bob_basis":   bob_basis,
        "bob_bit":     bob_bit,
        "eve_basis":   eve_basis,
        "eve_bit":     eve_bit,
        "basis_match": alice_basis == bob_basis,
    }

def run_bb84(n_bits: int, with_eve: bool, rng_seed: int | None = None) -> dict:
    if rng_seed is not None:
        np.random.seed(rng_seed)
        random.seed(rng_seed)

    alice_bits  = [random.randint(0, 1)        for _ in range(n_bits)]
    alice_bases = [random.choice(["Z", "X"])   for _ in range(n_bits)]
    bob_bases   = [random.choice(["Z", "X"])   for _ in range(n_bits)]
    eve_bases   = [random.choice(["Z", "X"]) if with_eve else None
                   for _ in range(n_bits)]

    qubit_states = []
    for i in range(n_bits):
        qd = simulate_qubit_bb84(
            alice_bits[i], alice_bases[i], bob_bases[i], eve_bases[i]
        )
        qubit_states.append(qd)

    sifted_alice, sifted_bob, sifted_idx = [], [], []
    for i, qd in enumerate(qubit_states):
        if qd["basis_match"]:
            sifted_alice.append(qd["alice_bit"])
            sifted_bob.append(qd["bob_bit"])
            sifted_idx.append(i)

    errors     = sum(a != b for a, b in zip(sifted_alice, sifted_bob))
    error_rate = errors / len(sifted_alice) if sifted_alice else 0.0

    eve_results = [qd["eve_bit"] for qd in qubit_states if qd["eve_bit"] is not None]

    return {
        "n_bits":       n_bits,
        "alice_bits":   alice_bits,
        "alice_bases":  alice_bases,
        "bob_bases":    bob_bases,
        "bob_results":  [qd["bob_bit"] for qd in qubit_states],
        "eve_results":  eve_results,
        "eve_bases":    [b for b in eve_bases if b is not None],
        "sifted_alice": sifted_alice,
        "sifted_bob":   sifted_bob,
        "sifted_idx":   sifted_idx,
        "errors":       errors,
        "error_rate":   error_rate,
        "qubit_states": qubit_states,
        "with_eve":     with_eve,
        "sim_label":    _SIM_LABEL,
    }


# ─── HTML helpers ─────────────────────────────────────────────────────────────
def render_qubit_grid(qstates, max_show=80):
    cells = []
    for i, q in enumerate(qstates[:max_show]):
        if not q["basis_match"]:
            cls, label = "qbit-discard", "⊘"
        elif q["alice_bit"] == q["bob_bit"]:
            cls, label = "qbit-match", str(q["alice_bit"])
        else:
            cls, label = "qbit-err", "✗"
        title = (
            f"Q{i}: Alice={q['alice_bit']}|{q['alice_basis']} "
            f"Bob={q['bob_bit']}|{q['bob_basis']}"
            + (f" Eve={q['eve_bit']}|{q['eve_basis']}" if q["eve_bit"] is not None else "")
        )
        cells.append(f'<div class="qbit {cls}" title="{title}">{label}</div>')
    if len(qstates) > max_show:
        cells.append(f'<div class="qbit qbit-discard">+{len(qstates)-max_show}</div>')
    return f'<div class="qbit-grid">{"".join(cells)}</div>'


def render_key_bits(bits, errs=None, max_show=64):
    out = []
    for i, b in enumerate(bits[:max_show]):
        cls = ("kb-x" if errs and i < len(errs) and errs[i]
               else ("kb-0" if b == 0 else "kb-1"))
        out.append(f'<div class="kb {cls}">{b}</div>')
    if len(bits) > max_show:
        out.append(f'<div class="kb kb-x">+{len(bits)-max_show}</div>')
    return f'<div class="key-bits">{"".join(out)}</div>'


def render_channel(with_eve: bool):
    mid = (
        '<div class="wire"></div>'
        '<div class="node node-eve">👁 EVE</div>'
        '<div class="wire"></div>'
        if with_eve else '<div class="wire"></div>'
    )
    return (
        f'<div class="channel">'
        f'<div class="node node-alice">⚛ ALICE</div>'
        f'{mid}'
        f'<div class="node node-bob">⚛ BOB</div>'
        f'</div>'
    )


def render_metrics(r):
    sn     = len(r["sifted_alice"])
    er     = r["error_rate"]
    secure = er < 0.11
    badge  = (
        '<span class="badge badge-secure">✓ SECURE</span>'
        if secure else
        '<span class="badge badge-abort">⚠ ABORT — EVE DETECTED</span>'
    )
    return f"""
    <div class="metric-row">
      <div class="metric-pill"><div class="val">{r['n_bits']}</div><div class="lbl">Qubits sent</div></div>
      <div class="metric-pill"><div class="val">{sn}</div><div class="lbl">Sifted key</div></div>
      <div class="metric-pill"><div class="val">{r['errors']}</div><div class="lbl">Errors</div></div>
      <div class="metric-pill">
        <div class="val" style="color:{'var(--accent3)' if not secure else 'var(--green)'}">
          {er:.1%}
        </div>
        <div class="lbl">QBER</div>
      </div>
    </div>
    <div style="margin-top:.5rem">{badge}</div>
    <div style="margin-top:.4rem;font-family:var(--font-mono);font-size:.62rem;color:var(--muted)">
      Backend: <span style="color:var(--accent1)">{r['sim_label']}</span>
    </div>
    """


def qber_bar(qber: float):
    pct   = min(qber * 100, 100)
    color = "#ff2d78" if qber >= 0.11 else ("#ffe600" if qber >= 0.05 else "#00ff9d")
    return f"""
    <div style="margin:.4rem 0">
      <div style="font-family:var(--font-mono);font-size:.65rem;color:var(--muted);letter-spacing:.15em;margin-bottom:4px">
        QBER  {qber:.1%}
        <span style="float:right;color:{color}">{'▲ ABOVE THRESHOLD' if qber>=.11 else '✓ SAFE'}</span>
      </div>
      <div style="background:rgba(255,255,255,.06);border-radius:4px;height:8px;overflow:hidden">
        <div style="height:100%;width:{pct:.1f}%;background:{color};border-radius:4px;transition:width .5s"></div>
      </div>
      <div style="font-family:var(--font-mono);font-size:.6rem;color:var(--muted);margin-top:3px">
        <span>0%</span>
        <span style="margin-left:calc(11% - 6px);color:rgba(255,230,0,.6)">│11%</span>
        <span style="float:right">100%</span>
      </div>
    </div>
    """


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Orbitron',sans-serif;font-size:.8rem;letter-spacing:.2em;
         color:#00e5ff;margin-bottom:1.2rem;padding-bottom:.6rem;border-bottom:1px solid rgba(0,229,255,.15)">
    PROTOCOL PARAMETERS
    </div>
    """, unsafe_allow_html=True)

    n_bits   = st.slider("Number of qubits", 10, 100, 40, step=10,
                         help="Keep ≤60 for snappy simulation with qsim")
    with_eve = st.checkbox("Enable Eve (eavesdropper)", value=False)
    seed_on  = st.checkbox("Fix random seed", value=False)
    seed_val = st.number_input("Seed value", value=42, step=1) if seed_on else None
    compare  = st.checkbox("Show No-Eve vs Eve comparison", value=False)

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn  = st.button("▶  RUN SIMULATION", use_container_width=True)

    st.markdown(f"""
    <div style="margin-top:2rem;font-family:'Share Tech Mono',monospace;font-size:.65rem;
         color:#4a6fa0;line-height:1.9;border-top:1px solid rgba(255,255,255,.05);padding-top:1rem">
    <b style="color:#00e5ff">BB84 PROTOCOL</b><br>
    Basis Z : {{|0⟩, |1⟩}}<br>
    Basis X : {{|+⟩, |−⟩}}<br>
    QBER threshold: 11%<br>
    Sifting: keep matching bases<br>
    Noise from Eve ≈ 25%<br><br>
    <b style="color:#00e5ff">BACKEND</b><br>
    <span style="color:#00ff9d">{_SIM_LABEL}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>BB84 QUANTUM KEY DISTRIBUTION</h1>
  <sub>Cirq + qsim Simulator</sub>
</div>
""", unsafe_allow_html=True)

if "result"     not in st.session_state: st.session_state.result     = None
if "result_eve" not in st.session_state: st.session_state.result_eve = None

if run_btn:
    prog = st.empty()
    steps = ["Preparing qubits…", "Building Cirq circuits…",
             "Running qsim…", "Sifting key…", "Computing QBER…"]
    for i, msg in enumerate(steps):
        prog.progress((i + 1) / len(steps), text=msg)
        time.sleep(0.18)
    prog.empty()

    with st.spinner("Simulating quantum channel with qsim…"):
        st.session_state.result = run_bb84(n_bits, with_eve, seed_val)
        if compare:
            st.session_state.result_eve = run_bb84(n_bits, True, seed_val)
        else:
            st.session_state.result_eve = None


r = st.session_state.result

if r is None:
    st.markdown("""
    <div class="q-card" style="text-align:center;padding:3rem;">
      <div style="font-size:3rem;margin-bottom:.8rem">⚛</div>
      <div style="font-family:'Orbitron',sans-serif;font-size:.9rem;letter-spacing:.25em;color:#00e5ff">
        AWAITING SIMULATION
      </div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:.72rem;color:#4a6fa0;margin-top:.5rem">
        Configure parameters in the sidebar and press RUN
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─── RESULTS ─────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1.1, 1], gap="medium")

with col_left:
    st.markdown(f"""
    <div class="q-card">
      <h3>Quantum Channel</h3>
      {render_channel(r['with_eve'])}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="q-card">
      <h3>Simulation Metrics</h3>
      {render_metrics(r)}
      {qber_bar(r['error_rate'])}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="q-card">
      <h3>Qubit Transmission Grid</h3>
      <div style="font-family:'Share Tech Mono',monospace;font-size:.63rem;color:#4a6fa0;margin-bottom:.6rem">
        <span style="color:#00ff9d">■</span> sifted-match &nbsp;
        <span style="color:#ff2d78">■</span> sifted-error &nbsp;
        <span style="color:#4a6fa0">■</span> discarded (basis mismatch) &nbsp; · hover for details
      </div>
      {render_qubit_grid(r['qubit_states'])}
    </div>
    """, unsafe_allow_html=True)

with col_right:
    err_mask = [a != b for a, b in zip(r["sifted_alice"], r["sifted_bob"])]
    st.markdown(f"""
    <div class="q-card">
      <h3>Alice's Sifted Key</h3>
      {render_key_bits(r['sifted_alice'], err_mask)}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="q-card">
      <h3>Bob's Sifted Key</h3>
      {render_key_bits(r['sifted_bob'], err_mask)}
    </div>
    """, unsafe_allow_html=True)


# ─── COMPARISON TABLE ─────────────────────────────────────────────────────────
if compare and st.session_state.result_eve:
    re = st.session_state.result_eve
    r0 = run_bb84(n_bits, False, seed_val)

    rows = [
        ("Qubits sent",   r0["n_bits"],              re["n_bits"]),
        ("Sifted length", len(r0["sifted_alice"]),   len(re["sifted_alice"])),
        ("Errors",        r0["errors"],              re["errors"]),
        ("QBER",          f"{r0['error_rate']:.2%}", f"{re['error_rate']:.2%}"),
        ("Status",
         "✓ SECURE" if r0["error_rate"] < 0.11 else "⚠ ABORT",
         "✓ SECURE" if re["error_rate"] < 0.11 else "⚠ EVE DETECTED"),
    ]

    def _row(label, v0, ve):
        ce = ('color:var(--accent3)' if 'EVE' in str(ve) or 'ABORT' in str(ve)
              else 'color:var(--green)' if 'SECURE' in str(ve) else '')
        return f"<tr><td style='color:var(--muted)'>{label}</td><td>{v0}</td><td style='{ce}'>{ve}</td></tr>"

    rows_html = "".join(_row(*row) for row in rows)

    st.markdown(f"""
    <div class="q-card" style="margin-top:.5rem">
      <h3>Scenario Comparison</h3>
      <table class="cmp-table">
        <tr><th>Metric</th><th>No Eve</th><th>With Eve</th></tr>
        {rows_html}
      </table>
    </div>
    """, unsafe_allow_html=True)

    cg1, cg2 = st.columns(2)
    with cg1:
        st.markdown(f"""
        <div class="q-card"><h3>No Eve · Qubit Grid</h3>
        {render_qubit_grid(r0['qubit_states'], 60)}</div>
        """, unsafe_allow_html=True)
    with cg2:
        st.markdown(f"""
        <div class="q-card"><h3>With Eve · Qubit Grid</h3>
        {render_qubit_grid(re['qubit_states'], 60)}</div>
        """, unsafe_allow_html=True)


st.markdown("""
<div style="text-align:center;margin-top:2rem;padding-top:1rem;
     border-top:1px solid rgba(0,229,255,.08);
     font-family:'Share Tech Mono',monospace;font-size:.62rem;color:#2a4060;letter-spacing:.12em">
</div>
""", unsafe_allow_html=True)