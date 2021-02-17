"""
Tests the Storage subclass
Command line: python -m pytest tests/unit/test_CPU.py
"""

import pytest

from app.models import inventory

@pytest.fixture
def storage_values():
    return {
        'name': 'Doggos',
        'manufacturer': 'Good_God',
        'total': 100,
        'allocated': 50,
        'capacity_GB': 2
    }

@pytest.fixture
def storage(storage_values):
    return inventory.Storage(**storage_values)

def test_create_storage(storage_values, storage):
    for attr_name in storage_values:
        assert getattr(storage, attr_name) == storage_values.get(attr_name)

@pytest.mark.parametrize(
    'gb, exception', [(10.5, TypeError), (-1, ValueError), (0, ValueError)]
)
def test_create_invalid_storage(gb, exception, storage_values):
    storage_values['capacity_GB'] = gb
    with pytest.raises(exception):
        inventory.Storage(**storage_values)

def test_repr(storage):
    assert storage.category in repr(storage)
    assert str(storage.capacity_GB) in repr(storage)