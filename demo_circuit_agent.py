#!/usr/bin/env python3
"""
Circuit Understanding AI - Interactive Demo

This script demonstrates the capabilities of the Circuit Understanding AI Agent
with various example circuits.
"""

from circuit_agent import CircuitAgent
from circuit_examples import ALL_EXAMPLES


def demo_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def demo_basic_usage():
    """Demonstrate basic usage"""
    demo_header("Demo 1: Basic Usage - LED Circuit")
    
    print("Circuit Netlist:")
    print(ALL_EXAMPLES['led_circuit'])
    
    agent = CircuitAgent()
    agent.parse_netlist(ALL_EXAMPLES['led_circuit'])
    agent.analyze_topology()
    agent.identify_circuit_type()
    
    print("\nGenerated Insights:")
    for insight in agent.get_insights():
        print(f"  • {insight}")


def demo_voltage_divider():
    """Demonstrate voltage divider analysis"""
    demo_header("Demo 2: Voltage Divider Analysis")
    
    agent = CircuitAgent()
    agent.parse_netlist(ALL_EXAMPLES['voltage_divider'])
    agent.analyze_topology()
    
    print(agent.generate_report())


def demo_filter_analysis():
    """Demonstrate filter circuit analysis"""
    demo_header("Demo 3: RC Filter Classification")
    
    print("Analyzing RC Low-Pass Filter...")
    agent = CircuitAgent()
    agent.parse_netlist(ALL_EXAMPLES['rc_filter'])
    agent.analyze_topology()
    circuit_type = agent.identify_circuit_type()
    
    print(f"\nCircuit Type: {circuit_type['primary_type'].upper()}")
    print(f"Confidence: {circuit_type['confidence']}")
    print(f"All matched patterns: {', '.join(circuit_type['all_matched_types'])}")
    
    topology = agent.analyze_topology()
    print(f"\nTopology Details:")
    print(f"  Components: {topology['total_components']}")
    print(f"  Nodes: {topology['nodes']}")
    print(f"  Component breakdown: {topology['component_breakdown']}")


def demo_amplifier():
    """Demonstrate amplifier circuit analysis"""
    demo_header("Demo 4: Transistor Amplifier Recognition")
    
    agent = CircuitAgent()
    agent.parse_netlist(ALL_EXAMPLES['common_emitter_amp'])
    agent.analyze_topology()
    circuit_type = agent.identify_circuit_type()
    
    print(f"Circuit identified as: {circuit_type['primary_type'].upper()}")
    
    print("\nComponent Analysis:")
    for comp_id, component in sorted(agent.components.items()):
        print(f"  {comp_id}: {component.type.value}")
        if component.value:
            print(f"    Value: {component.value}")


def demo_power_supply():
    """Demonstrate power supply circuit analysis"""
    demo_header("Demo 5: Power Supply Recognition")
    
    print("Comparing Half-Wave vs Full-Wave Rectifier:\n")
    
    circuits = [
        ('Half-Wave Rectifier', 'half_wave_rectifier'),
        ('Bridge Rectifier', 'bridge_rectifier')
    ]
    
    for name, key in circuits:
        agent = CircuitAgent()
        agent.parse_netlist(ALL_EXAMPLES[key])
        agent.analyze_topology()
        circuit_type = agent.identify_circuit_type()
        
        print(f"{name}:")
        print(f"  Type: {circuit_type['primary_type']}")
        print(f"  Components: {len(agent.components)}")
        
        comp_breakdown = agent._count_components_by_type()
        for comp_type, count in comp_breakdown.items():
            print(f"    - {count} {comp_type}(s)")
        print()


def demo_batch_analysis():
    """Demonstrate batch analysis of multiple circuits"""
    demo_header("Demo 6: Batch Analysis - All Example Circuits")
    
    results = []
    
    for name, netlist in ALL_EXAMPLES.items():
        agent = CircuitAgent()
        agent.parse_netlist(netlist)
        agent.analyze_topology()
        circuit_type = agent.identify_circuit_type()
        
        results.append({
            'name': name.replace('_', ' ').title(),
            'components': len(agent.components),
            'type': circuit_type['primary_type']
        })
    
    print(f"{'Circuit Name':<30} {'Components':<12} {'Type':<15}")
    print("-" * 70)
    for result in results:
        print(f"{result['name']:<30} {result['components']:<12} {result['type']:<15}")


def demo_interactive():
    """Interactive demo - analyze custom circuit"""
    demo_header("Demo 7: Interactive - Custom Circuit Analysis")
    
    print("Let's analyze a custom circuit:")
    print("\nExample - Simple Voltage Regulator:")
    
    custom_circuit = """
* 7805 Voltage Regulator Circuit
V1 1 0 DC 12V
C1 1 0 100u
U1 1 2 3 7805
C2 3 0 10u
R1 3 0 1k
"""
    
    print(custom_circuit)
    
    agent = CircuitAgent()
    agent.parse_netlist(custom_circuit)
    agent.analyze_topology()
    agent.identify_circuit_type()
    
    print(agent.generate_report())


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print(" " * 15 + "CIRCUIT UNDERSTANDING AI - DEMO")
    print("="*70)
    print("\nThis demo showcases the capabilities of the Circuit Understanding AI Agent")
    print("Analyzing various electronic circuits and providing intelligent insights")
    
    demos = [
        demo_basic_usage,
        demo_voltage_divider,
        demo_filter_analysis,
        demo_amplifier,
        demo_power_supply,
        demo_batch_analysis,
        demo_interactive,
    ]
    
    for demo in demos:
        try:
            demo()
            input("\nPress Enter to continue to next demo...")
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            break
    
    demo_header("Demo Complete!")
    print("Thank you for exploring the Circuit Understanding AI Agent!")
    print("\nTo learn more:")
    print("  • Read CIRCUIT_AGENT_GUIDE.md for comprehensive documentation")
    print("  • Check circuit_examples.py for 15+ example circuits")
    print("  • Run test_circuit_agent.py to see the test suite")
    print("\nHappy circuit analyzing! 🔌✨\n")


if __name__ == "__main__":
    main()
