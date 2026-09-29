# calculation-of-long-transmission-line
import cmath
import math

print("==============================================")
print("      LONG TRANSMISSION LINE CALCULATION")
print("        (Exact Distributed Parameter Model)")
print("==============================================")

# -------------------------------
# INPUT DATA
# -------------------------------

Vr_kV = float(input("Enter receiving-end line voltage (kV): "))
Ir = float(input("Enter receiving-end current (A): "))
pf = float(input("Enter receiving-end power factor (0 to 1): "))
length = float(input("Enter line length (km): "))

R_per_km = float(input("Enter resistance per km per phase (ohm/km): "))
L_per_km = float(input("Enter inductance per km per phase (mH/km): "))
C_per_km = float(input("Enter capacitance per km per phase (microF/km): "))

frequency = float(input("Enter frequency (Hz): "))

# -------------------------------
# RECEIVING-END QUANTITIES
# -------------------------------

Vr_line = Vr_kV * 1000
Vr_phase = Vr_line / math.sqrt(3)

# Power factor angle
phi = math.acos(pf)

# Assume lagging power factor
Ir_complex = Ir * cmath.exp(-1j * phi)

# -------------------------------
# DISTRIBUTED PARAMETERS
# -------------------------------

# Total resistance per phase
R = R_per_km * length

# Total inductance per phase
L = L_per_km * 1e-3 * length

# Total capacitance per phase
C_total = C_per_km * 1e-6 * length

# Angular frequency
omega = 2 * math.pi * frequency

# Series impedance per km
z = complex(
    R_per_km,
    omega * L_per_km * 1e-3
)

# Shunt admittance per km
y = complex(
    0,
    omega * C_per_km * 1e-6
)

# -------------------------------
# LONG LINE CONSTANTS
# -------------------------------

# Propagation constant
gamma = cmath.sqrt(z * y)

# Characteristic impedance
Zc = cmath.sqrt(z / y)

# Total propagation constant
gamma_l = gamma * length

# -------------------------------
# ABCD PARAMETERS
# -------------------------------

A = cmath.cosh(gamma_l)

B = Zc * cmath.sinh(gamma_l)

C_abcd = (1 / Zc) * cmath.sinh(gamma_l)

D = A

# -------------------------------
# SENDING-END VOLTAGE
# -------------------------------

Vs_phase = A * Vr_phase + B * Ir_complex

# Sending-end current
Is_complex = C_abcd * Vr_phase + D * Ir_complex

# Line voltage
Vs_line = abs(Vs_phase) * math.sqrt(3)

# Current magnitude
Is = abs(Is_complex)

# -------------------------------
# SENDING-END POWER
# -------------------------------

S_sending = 3 * Vs_phase * Is_complex.conjugate()

P_sending = S_sending.real
Q_sending = S_sending.imag

S_sending_mag = abs(S_sending)

pf_sending = abs(P_sending) / S_sending_mag

# -------------------------------
# RECEIVING-END POWER
# -------------------------------

P_receiving = (
    math.sqrt(3)
    * Vr_line
    * Ir
    * pf
)

S_receiving = (
    math.sqrt(3)
    * Vr_line
    * Ir
)

# -------------------------------
# VOLTAGE REGULATION
# -------------------------------

voltage_regulation = (
    (Vs_line - Vr_line) / Vr_line
) * 100

# -------------------------------
# POWER LOSS
# -------------------------------

power_loss = P_sending - P_receiving

# -------------------------------
# EFFICIENCY
# -------------------------------

efficiency = (
    P_receiving / P_sending
) * 100

# -------------------------------
# DISPLAY RESULTS
# -------------------------------

print("\n==============================================")
print("                 RESULTS")
print("==============================================")

print("\n--- LINE PARAMETERS ---")

print(f"Total resistance       : {R:.4f} ohm/phase")
print(f"Total inductance       : {L:.6f} H/phase")
print(f"Total capacitance      : {C_total * 1e6:.6f} microF/phase")

print("\n--- LONG LINE CONSTANTS ---")

print(f"Propagation constant γ : {gamma:.6e}")
print(f"Characteristic impedance Zc : {Zc:.4f} ohm")

print("\n--- ABCD PARAMETERS ---")

print(f"A = {A:.6f}")
print(f"B = {B:.6f}")
print(f"C = {C_abcd:.6e}")
print(f"D = {D:.6f}")

print("\n--- TRANSMISSION RESULTS ---")

print(f"Sending-end voltage    : {Vs_line / 1000:.4f} kV")
print(f"Sending-end current    : {Is:.4f} A")

print(f"Sending-end power      : {P_sending / 1000:.4f} kW")
print(f"Sending-end power factor : {pf_sending:.4f}")

print(f"Receiving-end power    : {P_receiving / 1000:.4f} kW")
print(f"Power loss             : {power_loss / 1000:.4f} kW")

print(f"Voltage regulation     : {voltage_regulation:.4f} %")
print(f"Efficiency             : {efficiency:.4f} %")

print("\n==============================================")
