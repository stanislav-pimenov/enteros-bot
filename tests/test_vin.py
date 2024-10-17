import pytest
from src.vin import validate_vin, InvalidVINException


# Test valid VINs
def test_valid_vin():
    valid_vins = [
        "1HGCM82633A004352",
        "JHMFA16586S012345",
        "2GCEC19T231319567",
        "WP0AB29922S686775",
        "3FAFP31351R120652"
    ]

    for vin in valid_vins:
        assert validate_vin(vin) == True


# Test invalid VINs (less than 17 characters, contains invalid characters, etc.)
def test_invalid_vin():
    invalid_vins = [
        "1HGCM82633A00435",  # Too short
        "JHMFA16586S01234O",  # Contains 'O'
        "2GCEC19T23131956!",  # Contains invalid symbol '!'
        "WP0AB2992S686775",  # Too short
        "3FAFP31351R120652Q"  # Contains 'Q'
    ]

    for vin in invalid_vins:
        with pytest.raises(InvalidVINException):
            validate_vin(vin)


# Test empty VIN
def test_empty_vin():
    with pytest.raises(InvalidVINException):
        validate_vin("")


# Test VIN with spaces
def test_vin_with_spaces():
    with pytest.raises(InvalidVINException):
        validate_vin("1HGCM82633A 04352")


# Test VIN with lowercase letters (should be uppercase)
def test_vin_with_lowercase():
    with pytest.raises(InvalidVINException):
        validate_vin("1hgcm82633a004352")
