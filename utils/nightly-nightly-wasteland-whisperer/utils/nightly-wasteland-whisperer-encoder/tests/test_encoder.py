import pytest
from unittest.mock import patch
import io
import argparse
from src.encoder import encode, decode, main, ENCODE_MAP, DECODE_MAP

def test_encode_basic_message():
    # Test basic encoding with lowercase letters
    message = "hello world"
    expected = "itllg vgksr"
    assert encode(message) == expected

def test_decode_basic_message():
    # Test basic decoding with lowercase letters
    message = "itllg vgksr"
    expected = "hello world"
    assert decode(message) == expected

def test_encode_with_uppercase():
    # Test encoding preserves uppercase characters
    message = "Hello World"
    expected = "Itllg Vgksr"
    assert encode(message) == expected

def test_decode_with_uppercase():
    # Test decoding preserves uppercase characters
    message = "Itllg Vgksr"
    expected = "Hello World"
    assert decode(message) == expected

def test_encode_with_numbers():
    # Test encoding with numbers
    message = "meet at 0800"
    expected = "dttt qz 5355"
    assert encode(message) == expected

def test_decode_with_numbers():
    # Test decoding with numbers
    message = "dttt qz 5355"
    expected = "meet at 0800"
    assert decode(message) == expected

def test_encode_with_punctuation_and_spaces():
    # Test encoding preserves punctuation and spaces
    message = "Hello, survivor! Meet me at the old bridge at 0800."
    expected = "Itllg, luvxixgx! Dttt dt xt zht glw wxiwht xt 5355."
    assert encode(message) == expected

def test_decode_with_punctuation_and_spaces():
    # Test decoding preserves punctuation and spaces
    message = "Itllg, luvxixgx! Dttt dt xt zht glw wxiwht xt 5355."
    expected = "Hello, survivor! Meet me at the old bridge at 0800."
    assert decode(message) == expected

def test_encode_empty_string():
    # Test encoding an empty string
    assert encode("") == ""

def test_decode_empty_string():
    # Test decoding an empty string
    assert decode("") == ""

def test_encode_unmapped_characters():
    # Test encoding with characters not in the map (e.g., symbols)
    message = "!@#$%^&*()_+"
    assert encode(message) == message

def test_decode_unmapped_characters():
    # Test decoding with characters not in the map
    message = "!@#$%^&*()_+"
    assert decode(message) == message

def test_encode_full_alphabet_and_numbers():
    # Test encoding the full alphabet and numbers
    alphabet_numbers = "abcdefghijklmnopqrstuvwxyz0123456789"
    expected_encoded = "qwert yuiopasdfghjklzxcvbnm5678901234"
    assert encode(alphabet_numbers) == expected_encoded

def test_decode_full_alphabet_and_numbers():
    # Test decoding the full alphabet and numbers
    encoded_alphabet_numbers = "qwert yuiopasdfghjklzxcvbnm5678901234"
    expected_decoded = "abcdefghijklmnopqrstuvwxyz0123456789"
    assert decode(encoded_alphabet_numbers) == expected_decoded

# Mock rationale: We need to test the main function's CLI behavior without actually
# running the command line or affecting sys.argv. patch('argparse.ArgumentParser.parse_args')
# allows us to simulate command-line arguments and test the output.
@patch('argparse.ArgumentParser.parse_args')
@patch('sys.stdout', new_callable=io.StringIO)
def test_main_encode_action(mock_stdout, mock_parse_args):
    # Simulate 'encode' action with a message
    test_message = 'test message'
    mock_parse_args.return_value = argparse.Namespace(action='encode', message=test_message)
    main()
    assert mock_stdout.getvalue().strip() == encode(test_message)

# Mock rationale: Same as above, for the 'decode' action.
@patch('argparse.ArgumentParser.parse_args')
@patch('sys.stdout', new_callable=io.StringIO)
def test_main_decode_action(mock_stdout, mock_parse_args):
    # Simulate 'decode' action with a message
    encoded_message = 'qtlz dtllqut'
    mock_parse_args.return_value = argparse.Namespace(action='decode', message=encoded_message)
    main()
    assert mock_stdout.getvalue().strip() == decode(encoded_message)

# Mock rationale: Test that the ENCODE_MAP and DECODE_MAP are inverses of each other.
# This is a crucial property for a cipher to work correctly.
def test_maps_are_inverses():
    for k, v in ENCODE_MAP.items():
        assert DECODE_MAP[v] == k
    for k, v in DECODE_MAP.items():
        assert ENCODE_MAP[v] == k
