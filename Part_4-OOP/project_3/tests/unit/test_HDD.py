"""
Tests the HDD subclass, which inherits from Storage
Command line: python -m pytest tests/unit/test_HDD.py
"""

import pytest

from app.models import inventory

@pytest.fixture
def hdd_values():
    return {
        'name': 'Doggos',
        'manufacturer': 'Good_God',
        'total': 100,
        'allocated': 50,
        'capacity_GB': 1,
        'size': '3.5"',
        'rpm': 3000
    }

@pytest.fixture
def hdd(hdd_values):
    return inventory.HDD(**hdd_values)

def test_create_hdd(hdd_values, hdd):
    for attr_name in hdd_values:
        assert getattr(hdd, attr_name) == hdd_values.get(attr_name)

@pytest.mark.parametrize('size', ['2.5', '5.25"'])
def test_create_invalid_size(size, hdd_values):
    hdd_values['size'] = size
    with pytest.raises(ValueError):
        inventory.HDD(**hdd_values)

@pytest.mark.parametrize(
    'rpm, exception',
    [
        ('100', TypeError),
        (100, ValueError),
        (100_000, ValueError)
    ]
)
def test_create_invalid_rpm(rpm, exception, hdd_values):
    hdd_values['rpm'] = rpm
    with pytest.raises(exception):
        inventory.HDD(**hdd_values)

def test_repr(hdd):
    assert hdd.category in repr(hdd)
    assert str(hdd.capacity_GB) in repr(hdd)
    assert hdd.size in repr(hdd)
    assert str(hdd.rpm) in repr(hdd)