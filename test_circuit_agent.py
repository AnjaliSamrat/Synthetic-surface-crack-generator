#!/usr/bin/env python3
"""
Tests for Circuit Understanding AI Agent

Run with: python test_circuit_agent.py
"""

import sys
from circuit_agent import CircuitAgent, ComponentType
from circuit_examples import ALL_EXAMPLES


def test_basic_parsing():
    """Test basic netlist parsing"""
    print("Testing: Basic Parsing...")
    
    netlist = """
V1 1 0 DC 5V
R1 1 2 1k
"""
    
    agent = CircuitAgent()
    result = agent.parse_netlist(netlist)
    
    assert result['success'] == True
    assert result['components'] == 2
    assert 'V1' in agent.components
    assert 'R1' in agent.components
    
    print("  ✓ Basic parsing works")


def test_component_identification():
    """Test component type identification"""
    print("Testing: Component Identification...")
    
    agent = CircuitAgent()
    
    test_cases = [
        ('R1', ComponentType.RESISTOR),
        ('C1', ComponentType.CAPACITOR),
        ('L1', ComponentType.INDUCTOR),
        ('D1', ComponentType.DIODE),
        ('Q1', ComponentType.TRANSISTOR),
        ('V1', ComponentType.VOLTAGE_SOURCE),
        ('I1', ComponentType.CURRENT_SOURCE),
        ('U1', ComponentType.IC),
    ]
    
    for comp_id, expected_type in test_cases:
        detected_type = agent._identify_component_type(comp_id)
        assert detected_type == expected_type, f"Failed for {comp_id}"
    
    print("  ✓ Component identification works")


def test_voltage_divider():
    """Test analysis of voltage divider circuit"""
    print("Testing: Voltage Divider Analysis...")
    
    agent = CircuitAgent()
    agent.parse_netlist(ALL_EXAMPLES['voltage_divider'])
    
    # Should have 3 components (V1, R1, R2)
    assert len(agent.components) == 3
    
    # Should detect resistors
    resistors = [c for c in agent.components.values() 
                 if c.type == ComponentType.RESISTOR]
    assert len(resistors) == 2
    
    topology = agent.analyze_topology()
    assert topology['total_components'] == 3
    
    print("  ✓ Voltage divider analysis works")


def test_rc_filter():
    """Test RC filter circuit recognition"""
    print("Testing: RC Filter Recognition...")
    
    agent = CircuitAgent()
    agent.parse_netlist(ALL_EXAMPLES['rc_filter'])
    
    # Should have R and C
    has_resistor = any(c.type == ComponentType.RESISTOR 
                      for c in agent.components.values())
    has_capacitor = any(c.type == ComponentType.CAPACITOR 
                       for c in agent.components.values())
    
    assert has_resistor and has_capacitor
    
    # Should be identified as filter
    circuit_type = agent.identify_circuit_type()
    assert 'filter' in circuit_type['all_matched_types']
    
    print("  ✓ RC filter recognition works")


def test_rectifier():
    """Test rectifier circuit recognition"""
    print("Testing: Rectifier Recognition...")
    
    agent = CircuitAgent()
    agent.parse_netlist(ALL_EXAMPLES['half_wave_rectifier'])
    
    # Should have diode and capacitor
    has_diode = any(c.type == ComponentType.DIODE 
                   for c in agent.components.values())
    has_capacitor = any(c.type == ComponentType.CAPACITOR 
                       for c in agent.components.values())
    
    assert has_diode and has_capacitor
    
    # Should be identified as power supply
    circuit_type = agent.identify_circuit_type()
    assert circuit_type['primary_type'] == 'power_supply'
    
    print("  ✓ Rectifier recognition works")


def test_amplifier():
    """Test amplifier circuit recognition"""
    print("Testing: Amplifier Recognition...")
    
    agent = CircuitAgent()
    agent.parse_netlist(ALL_EXAMPLES['common_emitter_amp'])
    
    # Should have transistor
    has_transistor = any(c.type == ComponentType.TRANSISTOR 
                        for c in agent.components.values())
    assert has_transistor
    
    # Should be identified as amplifier
    circuit_type = agent.identify_circuit_type()
    assert 'amplifier' in circuit_type['all_matched_types']
    
    print("  ✓ Amplifier recognition works")


def test_topology_analysis():
    """Test topology analysis features"""
    print("Testing: Topology Analysis...")
    
    # Test parallel components
    parallel_circuit = """
V1 1 0 DC 12V
R1 1 0 1k
R2 1 0 2k
"""
    
    agent = CircuitAgent()
    agent.parse_netlist(parallel_circuit)
    topology = agent.analyze_topology()
    
    # Should detect parallel resistors
    assert len(topology['parallel_components']) > 0
    
    print("  ✓ Topology analysis works")


def test_insights_generation():
    """Test insights generation"""
    print("Testing: Insights Generation...")
    
    agent = CircuitAgent()
    agent.parse_netlist(ALL_EXAMPLES['led_circuit'])
    agent.analyze_topology()
    agent.identify_circuit_type()
    
    insights = agent.get_insights()
    assert len(insights) > 0
    assert any('component' in i.lower() for i in insights)
    
    print("  ✓ Insights generation works")


def test_report_generation():
    """Test report generation"""
    print("Testing: Report Generation...")
    
    agent = CircuitAgent()
    agent.parse_netlist(ALL_EXAMPLES['voltage_divider'])
    agent.analyze_topology()
    
    report = agent.generate_report()
    
    assert 'CIRCUIT ANALYSIS REPORT' in report
    assert 'COMPONENTS:' in report
    assert 'CONNECTIONS:' in report
    assert 'INSIGHTS:' in report
    
    print("  ✓ Report generation works")


def test_all_examples():
    """Test that all example circuits can be parsed"""
    print("Testing: All Example Circuits...")
    
    for name, netlist in ALL_EXAMPLES.items():
        agent = CircuitAgent()
        result = agent.parse_netlist(netlist)
        assert result['success'], f"Failed to parse {name}"
    
    print(f"  ✓ All {len(ALL_EXAMPLES)} example circuits parse successfully")


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Circuit Understanding AI Agent - Test Suite")
    print("="*60)
    print()
    
    tests = [
        test_basic_parsing,
        test_component_identification,
        test_voltage_divider,
        test_rc_filter,
        test_rectifier,
        test_amplifier,
        test_topology_analysis,
        test_insights_generation,
        test_report_generation,
        test_all_examples,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Test error: {e}")
            failed += 1
    
    print()
    print("="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
