"""
Example Circuits for Circuit Understanding AI Agent

This file contains various example circuits in SPICE netlist format
that can be used to test and demonstrate the Circuit Agent.
"""

# Example 1: Simple LED Circuit
LED_CIRCUIT = """
* Simple LED Circuit with Current Limiting Resistor
V1 1 0 DC 5V
R1 1 2 330
D1 2 0 LED
"""

# Example 2: Voltage Divider
VOLTAGE_DIVIDER = """
* Voltage Divider Circuit
* Output voltage = Vin * (R2 / (R1 + R2))
V1 1 0 DC 12V
R1 1 2 10k
R2 2 0 10k
"""

# Example 3: RC Low-Pass Filter
RC_FILTER = """
* RC Low-Pass Filter
* Cutoff frequency = 1 / (2 * pi * R * C)
V1 1 0 AC 1V
R1 1 2 1k
C1 2 0 100n
"""

# Example 4: Half-Wave Rectifier
HALF_WAVE_RECTIFIER = """
* Half-Wave Rectifier (Simple Power Supply)
V1 1 0 AC 12V
D1 1 2 1N4007
C1 2 0 1000u
R1 2 0 1k
"""

# Example 5: Full-Wave Bridge Rectifier
BRIDGE_RECTIFIER = """
* Full-Wave Bridge Rectifier
V1 1 0 AC 12V
D1 1 2 1N4007
D2 0 2 1N4007
D3 3 1 1N4007
D4 3 0 1N4007
C1 2 3 1000u
R1 2 3 1k
"""

# Example 6: Common Emitter Amplifier
COMMON_EMITTER_AMP = """
* Common Emitter Amplifier
* Basic NPN transistor amplifier configuration
V1 1 0 DC 12V
R1 1 2 10k
R2 2 0 2k2
C1 3 2 10u
R3 1 4 1k
C2 4 5 10u
Q1 4 2 6 NPN
R4 6 0 100
C3 6 0 100u
"""

# Example 7: LC Oscillator
LC_OSCILLATOR = """
* LC Oscillator Circuit
V1 1 0 DC 5V
R1 1 2 1k
C1 2 3 100n
L1 3 4 1m
Q1 4 2 0 NPN
R2 2 0 10k
"""

# Example 8: 555 Timer Astable Circuit
TIMER_555_ASTABLE = """
* 555 Timer in Astable Mode
V1 1 0 DC 9V
R1 1 2 10k
R2 2 3 10k
C1 3 0 100n
C2 1 0 10u
U1 1 2 3 4 5 6 7 0 555
"""

# Example 9: Voltage Regulator
VOLTAGE_REGULATOR = """
* Simple Zener Voltage Regulator
V1 1 0 DC 15V
R1 1 2 100
D1 0 2 ZENER_5V1
R2 2 0 1k
"""

# Example 10: RC High-Pass Filter
RC_HIGH_PASS = """
* RC High-Pass Filter
V1 1 0 AC 1V
C1 1 2 100n
R1 2 0 1k
"""

# Example 11: Series RLC Circuit
SERIES_RLC = """
* Series RLC Circuit
V1 1 0 AC 1V
R1 1 2 100
L1 2 3 10m
C1 3 0 100n
"""

# Example 12: Parallel RLC Circuit
PARALLEL_RLC = """
* Parallel RLC Circuit
V1 1 0 AC 1V
R1 1 0 1k
L1 1 0 10m
C1 1 0 100n
"""

# Example 13: Inverting Op-Amp
INVERTING_OPAMP = """
* Inverting Op-Amp Configuration
V1 1 0 DC 12V
V2 0 2 DC 12V
R1 3 4 10k
R2 4 5 100k
U1 0 4 5 1 2 OPAMP
"""

# Example 14: LED Matrix Driver
LED_MATRIX = """
* Simple LED Matrix (2x2)
V1 1 0 DC 5V
R1 1 2 330
R2 1 3 330
D1 2 4 LED
D2 3 4 LED
D3 2 5 LED
D4 3 5 LED
"""

# Example 15: Push-Pull Amplifier
PUSH_PULL_AMP = """
* Push-Pull Amplifier
V1 1 0 DC 12V
Q1 1 2 3 NPN
Q2 3 2 0 PNP
R1 1 2 10k
R2 2 0 10k
C1 4 2 10u
R3 3 5 8
"""

# Dictionary of all examples
ALL_EXAMPLES = {
    "led_circuit": LED_CIRCUIT,
    "voltage_divider": VOLTAGE_DIVIDER,
    "rc_filter": RC_FILTER,
    "half_wave_rectifier": HALF_WAVE_RECTIFIER,
    "bridge_rectifier": BRIDGE_RECTIFIER,
    "common_emitter_amp": COMMON_EMITTER_AMP,
    "lc_oscillator": LC_OSCILLATOR,
    "timer_555": TIMER_555_ASTABLE,
    "voltage_regulator": VOLTAGE_REGULATOR,
    "rc_high_pass": RC_HIGH_PASS,
    "series_rlc": SERIES_RLC,
    "parallel_rlc": PARALLEL_RLC,
    "inverting_opamp": INVERTING_OPAMP,
    "led_matrix": LED_MATRIX,
    "push_pull_amp": PUSH_PULL_AMP,
}


def print_all_examples():
    """Print all example circuits"""
    for name, netlist in ALL_EXAMPLES.items():
        print(f"\n{'='*60}")
        print(f"Example: {name.replace('_', ' ').title()}")
        print('='*60)
        print(netlist)


if __name__ == "__main__":
    print("Circuit Examples Library")
    print("="*60)
    print(f"Total examples: {len(ALL_EXAMPLES)}")
    print("\nAvailable circuits:")
    for i, name in enumerate(ALL_EXAMPLES.keys(), 1):
        print(f"{i:2d}. {name.replace('_', ' ').title()}")
    
    print("\n" + "="*60)
    print("Use these examples with the Circuit Agent:")
    print("="*60)
    print("""
from circuit_agent import CircuitAgent
from examples import ALL_EXAMPLES

# Analyze any example
agent = CircuitAgent()
agent.parse_netlist(ALL_EXAMPLES['voltage_divider'])
agent.analyze_topology()
print(agent.generate_report())
""")
