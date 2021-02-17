"""
Tests the CPU subclass
Command line: python -m pytest tests/unit/test_CPU.py
"""

import pytest

from app.models import inventory

@pytest.fixture
def CPU_values():
    return {
        'name': 'Doggos',
        'manufacturer': 'Good_God',
        'total': 100,
        'allocated': 50,
        'cores': 1,
        'socket': 'woofer300',
        'power_watts': 300
    }

@pytest.fixture
def cpu(CPU_values):
    return inventory.CPU(**CPU_values)

def test_create_cpu(CPU_values, cpu):
    for attr_name in CPU_values:
        assert getattr(cpu, attr_name) == CPU_values.get(attr_name)

def test_create_invalid_cores_type():
    with pytest.raises(TypeError):
        inventory.CPU('name', 'manu', 100, 50, 0.5, 'sock', 98)

def test_create_invalid_power_type():
    with pytest.raises(TypeError):
        inventory.CPU('name', 'manu', 100, 50, 1, 'sock', 'pow')

@pytest.mark.parametrize('cores', [-2, 0])
def test_create_invalid_cores_value(cores):
    with pytest.raises(ValueError):
        inventory.CPU('name', 'manu', 100, 50, cores, 'sock', 98)

@pytest.mark.parametrize('power_watts', [-2, 0])
def test_create_invalid_power_value(power_watts):
    with pytest.raises(ValueError):
        inventory.CPU('name', 'manu', 100, 50, 1, 'sock', power_watts)

def test_repr(cpu):
    assert repr(cpu) == '{} ({} - {}) : total = {}, allocated = {}, cores = {}, socket = {}, power_watts = {}'.format(
        cpu.name, cpu.category, cpu.manufacturer, cpu.total,
        cpu.allocated, cpu.cores, cpu.socket, cpu.power_watts
    )