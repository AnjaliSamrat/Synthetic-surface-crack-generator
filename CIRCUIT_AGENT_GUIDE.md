# 🔌 Circuit Understanding AI Agent Guide

## Overview

The Circuit Understanding AI Agent is an intelligent system designed to analyze, understand, and provide insights about electronic circuits. It can parse circuit netlists, identify components, analyze topology, and classify circuit types.

## 🎯 Features

### Core Capabilities
- **Component Detection**: Automatically identify resistors, capacitors, inductors, transistors, ICs, and more
- **Topology Analysis**: Understand how components are connected (series, parallel)
- **Circuit Classification**: Identify circuit types (amplifier, power supply, filter, oscillator)
- **Netlist Parsing**: Support for SPICE-style netlist format
- **Connection Mapping**: Build a complete map of circuit connections
- **Insight Generation**: Provide human-readable insights about the circuit
- **Report Generation**: Create comprehensive analysis reports

### Supported Components
- Resistors (R)
- Capacitors (C)
- Inductors (L)
- Diodes (D)
- Transistors (Q)
- Integrated Circuits (U, X)
- Voltage Sources (V)
- Current Sources (I)
- Switches (S)
- Fuses (F)
- Transformers (T)

## 🚀 Quick Start

### Basic Usage

```python
from circuit_agent import CircuitAgent

# Create the AI agent
agent = CircuitAgent()

# Define your circuit netlist
netlist = """
* Simple LED Circuit
V1 1 0 DC 5V
R1 1 2 330
D1 2 0 LED
"""

# Parse the circuit
agent.parse_netlist(netlist)

# Analyze topology
topology = agent.analyze_topology()

# Identify circuit type
circuit_type = agent.identify_circuit_type()

# Get insights
insights = agent.get_insights()
for insight in insights:
    print(insight)

# Generate full report
print(agent.generate_report())
```

## 📚 Detailed Examples

### Example 1: Voltage Divider

```python
from circuit_agent import CircuitAgent

# Voltage divider circuit
voltage_divider = """
* Voltage Divider
V1 1 0 DC 12V
R1 1 2 10k
R2 2 0 10k
"""

agent = CircuitAgent()
agent.parse_netlist(voltage_divider)
agent.analyze_topology()

print(agent.generate_report())
```

**Output:**
```
============================================================
CIRCUIT ANALYSIS REPORT
============================================================

COMPONENTS:
----------------------------------------
R1: resistor = 10k (nodes: 1, 2)
R2: resistor = 10k (nodes: 2, 0)
V1: voltage_source = DC 12V (nodes: 1, 0)

CONNECTIONS:
----------------------------------------
Node 0: V1, R2
Node 1: V1, R1
Node 2: R1, R2

INSIGHTS:
----------------------------------------
Circuit contains 3 components
- 2 resistor(s)
- 1 voltage_source(s)
Found 3 series connections

============================================================
```

### Example 2: RC Filter

```python
# Low-pass RC filter
rc_filter = """
* RC Low-Pass Filter
V1 1 0 AC 1V
R1 1 2 1k
C1 2 0 100n
"""

agent = CircuitAgent()
agent.parse_netlist(rc_filter)
topology = agent.analyze_topology()
circuit_type = agent.identify_circuit_type()

print(f"Circuit Type: {circuit_type['primary_type']}")
# Output: Circuit Type: filter
```

### Example 3: Transistor Amplifier

```python
# Simple transistor amplifier
amplifier = """
* Common Emitter Amplifier
V1 1 0 DC 12V
R1 1 2 10k
R2 2 0 2k
C1 3 2 10u
R3 1 4 1k
C2 4 5 10u
Q1 4 2 6 NPN
R4 6 0 100
"""

agent = CircuitAgent()
agent.parse_netlist(amplifier)
agent.analyze_topology()
circuit_type = agent.identify_circuit_type()

insights = agent.get_insights()
for insight in insights:
    print(insight)
```

## 🔧 Advanced Usage

### Exporting Analysis to JSON

```python
agent = CircuitAgent()
agent.parse_netlist(your_netlist)
agent.analyze_topology()
agent.identify_circuit_type()

# Export complete analysis
agent.export_to_json("circuit_analysis.json")
```

### Programmatic Access to Components

```python
agent = CircuitAgent()
agent.parse_netlist(netlist)

# Access all components
for comp_id, component in agent.components.items():
    print(f"{comp_id}: {component.type.value}")
    print(f"  Nodes: {component.nodes}")
    print(f"  Value: {component.value}")

# Access specific components
resistors = [c for c in agent.components.values() 
             if c.type == ComponentType.RESISTOR]
```

### Analyzing Connections

```python
agent = CircuitAgent()
agent.parse_netlist(netlist)

# Get all connections
for node_id, connection in agent.connections.items():
    print(f"Node {node_id} connects:")
    for comp_id in connection.components:
        comp = agent.components[comp_id]
        print(f"  - {comp_id} ({comp.type.value})")
```

## 🎓 Use Cases

### 1. Educational Tool
Help students learn circuit analysis by providing automatic insights:
```python
# Student uploads their circuit design
agent = CircuitAgent()
agent.parse_netlist(student_circuit)
agent.analyze_topology()

# Provide feedback
insights = agent.get_insights()
print("Circuit Feedback:")
for insight in insights:
    print(f"✓ {insight}")
```

### 2. Circuit Validation
Validate circuit designs before PCB manufacturing:
```python
agent = CircuitAgent()
agent.parse_netlist(design_netlist)
topology = agent.analyze_topology()

# Check for common issues
if topology['total_components'] == 0:
    print("⚠️ Warning: No components found!")

if topology['nodes'] < 2:
    print("⚠️ Warning: Circuit may be incomplete")
```

### 3. Documentation Generator
Automatically generate circuit documentation:
```python
agent = CircuitAgent()
agent.parse_netlist(circuit_netlist)
agent.analyze_topology()
circuit_type = agent.identify_circuit_type()

# Generate documentation
doc = f"""
# Circuit Documentation

## Type
{circuit_type['primary_type'].title()}

## Analysis
{agent.generate_report()}
"""

with open("circuit_doc.md", "w") as f:
    f.write(doc)
```

### 4. Circuit Comparison
Compare different circuit variations:
```python
def compare_circuits(netlist1, netlist2):
    agent1 = CircuitAgent()
    agent2 = CircuitAgent()
    
    agent1.parse_netlist(netlist1)
    agent2.parse_netlist(netlist2)
    
    agent1.analyze_topology()
    agent2.analyze_topology()
    
    print(f"Circuit 1: {len(agent1.components)} components")
    print(f"Circuit 2: {len(agent2.components)} components")
```

## 🛠️ Netlist Format

The agent supports SPICE-style netlists. Basic format:

```
* Comments start with asterisk
ComponentID Node1 Node2 [Node3...] Value

Examples:
R1 1 2 1k          # Resistor from node 1 to 2, value 1kΩ
C1 3 0 100u        # Capacitor from node 3 to ground, 100µF
V1 1 0 DC 5V       # Voltage source, 5V DC
Q1 1 2 3 NPN       # Transistor (collector, base, emitter)
D1 2 3 LED         # Diode/LED
```

### Component Naming Convention
- **R**: Resistor (e.g., R1, R2)
- **C**: Capacitor (e.g., C1, C2)
- **L**: Inductor (e.g., L1, L2)
- **D**: Diode (e.g., D1, D2)
- **Q**: Transistor (e.g., Q1, Q2)
- **V**: Voltage Source (e.g., V1, V2)
- **I**: Current Source (e.g., I1, I2)
- **U** or **X**: IC (e.g., U1, X1)

### Value Notation
- **k**: kilo (1k = 1000)
- **M**: mega (1M = 1,000,000)
- **m**: milli (1m = 0.001)
- **u**: micro (1u = 0.000001)
- **n**: nano (1n = 0.000000001)
- **p**: pico (1p = 0.000000000001)

## 📊 Circuit Types Recognized

The AI agent can identify the following circuit types:

1. **Power Supply**
   - Contains: Diodes, capacitors, (transformers)
   - Function: Convert AC to DC, regulate voltage

2. **Amplifier**
   - Contains: Transistors, resistors, capacitors
   - Function: Increase signal amplitude

3. **Filter**
   - Contains: Resistors, capacitors, and/or inductors
   - Function: Pass/block specific frequencies

4. **Oscillator**
   - Contains: Transistors, capacitors/inductors
   - Function: Generate periodic signals

5. **Digital Logic**
   - Contains: Integrated circuits
   - Function: Digital signal processing

## 🎯 Integration with Other Tools

### Using with Circuit Simulators

```python
# After simulation, analyze the circuit
import circuit_agent

agent = circuit_agent.CircuitAgent()
agent.parse_netlist(simulation_netlist)
agent.analyze_topology()

# Get insights for optimization
insights = agent.get_insights()
```

### Integration with Web Apps

```python
from flask import Flask, request, jsonify
from circuit_agent import CircuitAgent

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_circuit():
    netlist = request.json['netlist']
    
    agent = CircuitAgent()
    agent.parse_netlist(netlist)
    agent.analyze_topology()
    circuit_type = agent.identify_circuit_type()
    
    return jsonify({
        'insights': agent.get_insights(),
        'type': circuit_type['primary_type'],
        'report': agent.generate_report()
    })
```

## 🧪 Testing Your Circuits

Run the example script:

```bash
python circuit_agent.py
```

Create your own test:

```python
from circuit_agent import CircuitAgent

# Your circuit netlist
my_circuit = """
* My Custom Circuit
V1 1 0 DC 9V
R1 1 2 1k
LED1 2 0 LED
"""

agent = CircuitAgent()
agent.parse_netlist(my_circuit)
agent.analyze_topology()
print(agent.generate_report())
```

## 💡 Tips and Best Practices

1. **Node Numbering**: Use node 0 for ground
2. **Component Values**: Include units for clarity (1k, 100u, etc.)
3. **Comments**: Add comments with `*` for documentation
4. **Validation**: Always check parsing results before analysis
5. **JSON Export**: Use JSON export for integration with other tools

## 🔍 Troubleshooting

### Issue: Components Not Detected
```python
# Check parsing results
result = agent.parse_netlist(netlist)
print(f"Parsed {result['components']} components")

# List all detected components
for comp_id in agent.components:
    print(comp_id)
```

### Issue: Incorrect Circuit Type
```python
# Get all matched types
circuit_type = agent.identify_circuit_type()
print(f"All matches: {circuit_type['all_matched_types']}")

# The circuit may match multiple patterns
```

### Issue: Missing Connections
```python
# Debug connections
topology = agent.analyze_topology()
print(f"Nodes: {topology['nodes']}")

for node_id, conn in agent.connections.items():
    print(f"{node_id}: {conn.components}")
```

## 🚀 Future Enhancements

Planned features:
- [ ] Visual circuit diagram generation
- [ ] AC/DC analysis
- [ ] Component recommendation
- [ ] PCB layout suggestions
- [ ] Machine learning-based circuit optimization
- [ ] Support for more netlist formats
- [ ] Real-time circuit simulation

## 📖 Additional Resources

- SPICE Netlist Format: [Wikipedia](https://en.wikipedia.org/wiki/SPICE)
- Circuit Analysis Basics: [All About Circuits](https://www.allaboutcircuits.com/)
- Electronic Components: [Electronics Tutorials](https://www.electronics-tutorials.ws/)

## 🤝 Contributing

Have ideas for improving the circuit agent? Contributions welcome!

```bash
# Clone the repository
git clone https://github.com/AnjaliSamrat/Synthetic-surface-crack-generator.git

# Add your improvements
# Submit a pull request
```

## 📄 License

Open source for educational purposes.

---

**Ready to analyze circuits?** Start with the examples above and explore the capabilities of the Circuit Understanding AI Agent!
