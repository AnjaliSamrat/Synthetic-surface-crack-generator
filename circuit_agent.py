#!/usr/bin/env python3
"""
Circuit Understanding AI Agent

An AI agent that analyzes and understands electronic circuits, providing insights
about circuit topology, component relationships, and functionality.

Features:
- Circuit component detection and classification
- Topology analysis
- Circuit functionality inference
- Component value extraction
- Connection mapping
"""

import json
import re
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum


class ComponentType(Enum):
    """Types of electronic components"""
    RESISTOR = "resistor"
    CAPACITOR = "capacitor"
    INDUCTOR = "inductor"
    DIODE = "diode"
    TRANSISTOR = "transistor"
    LED = "led"
    IC = "integrated_circuit"
    VOLTAGE_SOURCE = "voltage_source"
    CURRENT_SOURCE = "current_source"
    GROUND = "ground"
    SWITCH = "switch"
    FUSE = "fuse"
    TRANSFORMER = "transformer"
    UNKNOWN = "unknown"


@dataclass
class Component:
    """Represents an electronic component"""
    id: str
    type: ComponentType
    value: Optional[str] = None
    nodes: List[str] = None
    properties: Dict = None
    
    def __post_init__(self):
        if self.nodes is None:
            self.nodes = []
        if self.properties is None:
            self.properties = {}


@dataclass
class Connection:
    """Represents a connection between components"""
    node_id: str
    components: List[str]
    
    def __post_init__(self):
        if self.components is None:
            self.components = []


class CircuitAgent:
    """
    AI Agent for understanding electronic circuits.
    
    This agent can:
    - Parse circuit netlists
    - Analyze circuit topology
    - Identify circuit functionality
    - Provide insights and recommendations
    """
    
    def __init__(self):
        self.components: Dict[str, Component] = {}
        self.connections: Dict[str, Connection] = {}
        self.analysis_results: Dict = {}
    
    def parse_netlist(self, netlist: str) -> Dict:
        """
        Parse a SPICE-style netlist.
        
        Args:
            netlist: Circuit netlist in SPICE format
            
        Returns:
            Dictionary with parsing results
        """
        self.components.clear()
        self.connections.clear()
        
        lines = netlist.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('*') or line.startswith('.'):
                continue
            
            self._parse_component_line(line)
        
        self._build_connections()
        
        return {
            "components": len(self.components),
            "connections": len(self.connections),
            "success": True
        }
    
    def _parse_component_line(self, line: str):
        """Parse a single component line from netlist"""
        parts = line.split()
        if len(parts) < 2:
            return
        
        component_id = parts[0]
        component_type = self._identify_component_type(component_id)
        
        # Extract nodes (typically positions 1 and 2, or more for ICs)
        nodes = []
        value = None
        
        if component_type in [ComponentType.RESISTOR, ComponentType.CAPACITOR, 
                               ComponentType.INDUCTOR]:
            if len(parts) >= 3:
                nodes = parts[1:3]
                value = parts[3] if len(parts) > 3 else None
        elif component_type == ComponentType.DIODE:
            if len(parts) >= 3:
                nodes = parts[1:3]
        elif component_type == ComponentType.TRANSISTOR:
            if len(parts) >= 4:
                nodes = parts[1:4]
        elif component_type in [ComponentType.VOLTAGE_SOURCE, ComponentType.CURRENT_SOURCE]:
            if len(parts) >= 3:
                nodes = parts[1:3]
                value = parts[3] if len(parts) > 3 else None
        
        component = Component(
            id=component_id,
            type=component_type,
            value=value,
            nodes=nodes
        )
        
        self.components[component_id] = component
    
    def _identify_component_type(self, component_id: str) -> ComponentType:
        """Identify component type from its ID prefix"""
        prefix = component_id[0].upper() if component_id else ''
        
        type_map = {
            'R': ComponentType.RESISTOR,
            'C': ComponentType.CAPACITOR,
            'L': ComponentType.INDUCTOR,
            'D': ComponentType.DIODE,
            'Q': ComponentType.TRANSISTOR,
            'V': ComponentType.VOLTAGE_SOURCE,
            'I': ComponentType.CURRENT_SOURCE,
            'U': ComponentType.IC,
            'X': ComponentType.IC,
            'S': ComponentType.SWITCH,
            'F': ComponentType.FUSE,
            'T': ComponentType.TRANSFORMER,
        }
        
        return type_map.get(prefix, ComponentType.UNKNOWN)
    
    def _build_connections(self):
        """Build connection map from components"""
        node_components: Dict[str, List[str]] = {}
        
        for comp_id, component in self.components.items():
            for node in component.nodes:
                if node not in node_components:
                    node_components[node] = []
                node_components[node].append(comp_id)
        
        for node_id, comp_list in node_components.items():
            self.connections[node_id] = Connection(
                node_id=node_id,
                components=comp_list
            )
    
    def analyze_topology(self) -> Dict:
        """
        Analyze circuit topology.
        
        Returns:
            Dictionary with topology analysis
        """
        analysis = {
            "total_components": len(self.components),
            "component_breakdown": self._count_components_by_type(),
            "nodes": len(self.connections),
            "series_components": self._find_series_components(),
            "parallel_components": self._find_parallel_components(),
        }
        
        self.analysis_results["topology"] = analysis
        return analysis
    
    def _count_components_by_type(self) -> Dict[str, int]:
        """Count components by type"""
        counts = {}
        for component in self.components.values():
            type_name = component.type.value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts
    
    def _find_series_components(self) -> List[List[str]]:
        """Find components connected in series"""
        series_groups = []
        
        for node_id, connection in self.connections.items():
            if len(connection.components) == 2:
                # Two components connected at a single node (potentially series)
                series_groups.append(connection.components)
        
        return series_groups
    
    def _find_parallel_components(self) -> List[List[str]]:
        """Find components connected in parallel"""
        parallel_groups = []
        
        # Group components by their node pairs
        node_pairs = {}
        for comp_id, component in self.components.items():
            if len(component.nodes) == 2:
                nodes = tuple(sorted(component.nodes))
                if nodes not in node_pairs:
                    node_pairs[nodes] = []
                node_pairs[nodes].append(comp_id)
        
        # Find groups with multiple components
        for nodes, components in node_pairs.items():
            if len(components) > 1:
                parallel_groups.append(components)
        
        return parallel_groups
    
    def identify_circuit_type(self) -> Dict:
        """
        Identify the type of circuit based on components and topology.
        
        Returns:
            Dictionary with circuit classification
        """
        component_types = set(c.type for c in self.components.values())
        
        circuit_patterns = {
            "power_supply": self._is_power_supply(),
            "amplifier": self._is_amplifier(),
            "filter": self._is_filter(),
            "oscillator": self._is_oscillator(),
            "digital_logic": self._is_digital_logic(),
        }
        
        identified_types = [k for k, v in circuit_patterns.items() if v]
        
        result = {
            "primary_type": identified_types[0] if identified_types else "unknown",
            "all_matched_types": identified_types,
            "confidence": "high" if identified_types else "low"
        }
        
        self.analysis_results["circuit_type"] = result
        return result
    
    def _is_power_supply(self) -> bool:
        """Check if circuit is a power supply"""
        has_diode = any(c.type == ComponentType.DIODE for c in self.components.values())
        has_capacitor = any(c.type == ComponentType.CAPACITOR for c in self.components.values())
        has_transformer = any(c.type == ComponentType.TRANSFORMER for c in self.components.values())
        
        return has_diode and has_capacitor
    
    def _is_amplifier(self) -> bool:
        """Check if circuit is an amplifier"""
        has_transistor = any(c.type == ComponentType.TRANSISTOR for c in self.components.values())
        has_resistor = any(c.type == ComponentType.RESISTOR for c in self.components.values())
        has_capacitor = any(c.type == ComponentType.CAPACITOR for c in self.components.values())
        
        return has_transistor and has_resistor
    
    def _is_filter(self) -> bool:
        """Check if circuit is a filter"""
        has_capacitor = any(c.type == ComponentType.CAPACITOR for c in self.components.values())
        has_inductor = any(c.type == ComponentType.INDUCTOR for c in self.components.values())
        has_resistor = any(c.type == ComponentType.RESISTOR for c in self.components.values())
        
        return (has_capacitor or has_inductor) and has_resistor
    
    def _is_oscillator(self) -> bool:
        """Check if circuit is an oscillator"""
        has_transistor = any(c.type == ComponentType.TRANSISTOR for c in self.components.values())
        has_capacitor = any(c.type == ComponentType.CAPACITOR for c in self.components.values())
        has_inductor = any(c.type == ComponentType.INDUCTOR for c in self.components.values())
        
        return has_transistor and (has_capacitor or has_inductor)
    
    def _is_digital_logic(self) -> bool:
        """Check if circuit is digital logic"""
        has_ic = any(c.type == ComponentType.IC for c in self.components.values())
        return has_ic
    
    def get_insights(self) -> List[str]:
        """
        Generate insights about the circuit.
        
        Returns:
            List of insight strings
        """
        insights = []
        
        # Component insights
        comp_breakdown = self._count_components_by_type()
        total_components = len(self.components)
        
        insights.append(f"Circuit contains {total_components} components")
        
        for comp_type, count in comp_breakdown.items():
            if count > 0:
                insights.append(f"- {count} {comp_type}(s)")
        
        # Topology insights
        if "topology" in self.analysis_results:
            topo = self.analysis_results["topology"]
            if topo.get("series_components"):
                insights.append(f"Found {len(topo['series_components'])} series connections")
            if topo.get("parallel_components"):
                insights.append(f"Found {len(topo['parallel_components'])} parallel groups")
        
        # Circuit type insights
        if "circuit_type" in self.analysis_results:
            circuit_type = self.analysis_results["circuit_type"]
            if circuit_type["primary_type"] != "unknown":
                insights.append(f"Circuit appears to be a {circuit_type['primary_type']}")
        
        return insights
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive report about the circuit.
        
        Returns:
            Formatted report string
        """
        report_lines = [
            "=" * 60,
            "CIRCUIT ANALYSIS REPORT",
            "=" * 60,
            ""
        ]
        
        # Components section
        report_lines.append("COMPONENTS:")
        report_lines.append("-" * 40)
        for comp_id, component in sorted(self.components.items()):
            value_str = f" = {component.value}" if component.value else ""
            nodes_str = f" (nodes: {', '.join(component.nodes)})" if component.nodes else ""
            report_lines.append(f"{comp_id}: {component.type.value}{value_str}{nodes_str}")
        report_lines.append("")
        
        # Connections section
        report_lines.append("CONNECTIONS:")
        report_lines.append("-" * 40)
        for node_id, connection in sorted(self.connections.items()):
            components_str = ", ".join(connection.components)
            report_lines.append(f"Node {node_id}: {components_str}")
        report_lines.append("")
        
        # Insights section
        report_lines.append("INSIGHTS:")
        report_lines.append("-" * 40)
        for insight in self.get_insights():
            report_lines.append(insight)
        report_lines.append("")
        
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def export_to_json(self, filepath: str):
        """Export circuit data to JSON file"""
        data = {
            "components": {
                comp_id: {
                    "type": comp.type.value,
                    "value": comp.value,
                    "nodes": comp.nodes,
                    "properties": comp.properties
                }
                for comp_id, comp in self.components.items()
            },
            "connections": {
                node_id: conn.components
                for node_id, conn in self.connections.items()
            },
            "analysis": self.analysis_results
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    """Example usage of the Circuit Agent"""
    
    # Example netlist (simple voltage divider)
    example_netlist = """
* Voltage Divider Circuit
V1 1 0 DC 12V
R1 1 2 10k
R2 2 0 10k
    """
    
    print("Circuit Understanding AI Agent")
    print("=" * 60)
    print()
    
    # Create agent
    agent = CircuitAgent()
    
    # Parse netlist
    print("Parsing netlist...")
    result = agent.parse_netlist(example_netlist)
    print(f"✓ Parsed {result['components']} components, {result['connections']} nodes")
    print()
    
    # Analyze topology
    print("Analyzing topology...")
    topology = agent.analyze_topology()
    print(f"✓ Topology analysis complete")
    print()
    
    # Identify circuit type
    print("Identifying circuit type...")
    circuit_type = agent.identify_circuit_type()
    print(f"✓ Circuit type: {circuit_type['primary_type']}")
    print()
    
    # Generate report
    print(agent.generate_report())


if __name__ == "__main__":
    main()
