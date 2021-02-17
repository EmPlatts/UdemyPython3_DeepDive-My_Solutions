"""
Tests the SSD subclass, which inherits from Storage
Command line: python -m pytest tests/unit/test_SSD.py
"""

import pytest

from app.models import inventory

@pytest.fixture
def ssd_values():
    return {
        'name': 'Doggos',
        'manufacturer': 'Good_God',
        'total': 100,
        'allocated': 50,
        'capacity_GB': 1,
        'interface': 'PCIe NVMe 3.0 x4'
    }

@pytest.fixture
def ssd(ssd_values):
    return inventory.SSD(**ssd_values)

def test_create_ssd(ssd_values, ssd):
    for attr_name in ssd_values:
        assert getattr(ssd, attr_name) == ssd_values.get(attr_name)

def test_repr(ssd):
    assert ssd.category in repr(ssd)
    assert str(ssd.capacity_GB) in repr(ssd)
    assert ssd.interface in repr(ssd)