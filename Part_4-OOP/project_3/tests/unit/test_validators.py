"""
Tests the validator functions
Command line: python -m pytest tests/unit/test_validators.py
"""

import pytest
from app.utils.validators import validate_integer

class TestIntegerValidator:
    def test_valid(self):
       validate_integer('arg', 10, 0, 20, 'custom min msg', 'custom max msg')
        
    def test_type_error(self):
        with pytest.raises(TypeError):
            validate_integer('arg', 1.5)
    
    def test_default_min_error(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, 100)
        assert 'arg' in str(ex.value)
        assert '100' in str(ex.value)

    def test_default_max_error(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, 0, 5)
        assert 'arg' in str(ex.value)
        assert '5' in str(ex.value)

    def test_custom_min_error(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, 100, custom_min_message='custom')
        assert str(ex.value) == 'custom'

    def test_custom_max_error(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, 0, 5, custom_max_message='custom')
        assert str(ex.value) == 'custom'
        