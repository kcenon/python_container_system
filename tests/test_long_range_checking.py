"""
Test long/ulong type range checking policy.

Tests the unified long type policy implementation:
- LongValue (type 6): must fit in 32-bit signed range
- ULongValue (type 7): must fit in 32-bit unsigned range
- Values exceeding range should raise OverflowError
"""

import unittest
import struct
from container_module.values.numeric_value import (
    LongValue,
    ULongValue,
    LLongValue,
    ULLongValue,
)


class TestLongRangeChecking(unittest.TestCase):
    """Test suite for long/ulong range checking."""

    # 32-bit boundary values
    INT32_MIN = -(2**31)
    INT32_MAX = 2**31 - 1
    UINT32_MAX = 2**32 - 1

    # ========================================================================
    # LongValue (type 6) Tests - Signed 32-bit Range
    # ========================================================================

    def test_long_value_accepts_valid_positive_value(self):
        """LongValue should accept valid positive values."""
        lv = LongValue("test", 1000000)
        self.assertEqual(lv.to_long(), 1000000)

    def test_long_value_accepts_valid_negative_value(self):
        """LongValue should accept valid negative values."""
        lv = LongValue("test", -1000000)
        self.assertEqual(lv.to_long(), -1000000)

    def test_long_value_accepts_zero(self):
        """LongValue should accept zero."""
        lv = LongValue("test", 0)
        self.assertEqual(lv.to_long(), 0)

    def test_long_value_accepts_int32_max(self):
        """LongValue should accept INT32_MAX."""
        lv = LongValue("test", self.INT32_MAX)
        self.assertEqual(lv.to_long(), self.INT32_MAX)

    def test_long_value_accepts_int32_min(self):
        """LongValue should accept INT32_MIN."""
        lv = LongValue("test", self.INT32_MIN)
        self.assertEqual(lv.to_long(), self.INT32_MIN)

    def test_long_value_rejects_int32_max_plus_one(self):
        """LongValue should reject INT32_MAX + 1."""
        with self.assertRaises(OverflowError) as cm:
            LongValue("test", self.INT32_MAX + 1)
        self.assertIn("32-bit range", str(cm.exception))
        self.assertIn("LLongValue", str(cm.exception))

    def test_long_value_rejects_int32_min_minus_one(self):
        """LongValue should reject INT32_MIN - 1."""
        with self.assertRaises(OverflowError) as cm:
            LongValue("test", self.INT32_MIN - 1)
        self.assertIn("32-bit range", str(cm.exception))

    def test_long_value_rejects_large_positive_value(self):
        """LongValue should reject large positive values (e.g., 5 billion)."""
        with self.assertRaises(OverflowError):
            LongValue("test", 5000000000)

    def test_long_value_rejects_large_negative_value(self):
        """LongValue should reject large negative values (e.g., -5 billion)."""
        with self.assertRaises(OverflowError):
            LongValue("test", -5000000000)

    # ========================================================================
    # ULongValue (type 7) Tests - Unsigned 32-bit Range
    # ========================================================================

    def test_ulong_value_accepts_valid_value(self):
        """ULongValue should accept valid values."""
        ulv = ULongValue("test", 1000000)
        self.assertEqual(ulv.to_ulong(), 1000000)

    def test_ulong_value_accepts_zero(self):
        """ULongValue should accept zero."""
        ulv = ULongValue("test", 0)
        self.assertEqual(ulv.to_ulong(), 0)

    def test_ulong_value_accepts_uint32_max(self):
        """ULongValue should accept UINT32_MAX."""
        ulv = ULongValue("test", self.UINT32_MAX)
        self.assertEqual(ulv.to_ulong(), self.UINT32_MAX)

    def test_ulong_value_rejects_negative_value(self):
        """ULongValue should reject negative values."""
        with self.assertRaises(OverflowError) as cm:
            ULongValue("test", -1)
        self.assertIn("32-bit range", str(cm.exception))

    def test_ulong_value_rejects_uint32_max_plus_one(self):
        """ULongValue should reject UINT32_MAX + 1."""
        with self.assertRaises(OverflowError) as cm:
            ULongValue("test", self.UINT32_MAX + 1)
        self.assertIn("32-bit range", str(cm.exception))
        self.assertIn("ULLongValue", str(cm.exception))

    def test_ulong_value_rejects_large_value(self):
        """ULongValue should reject large values (e.g., 10 billion)."""
        with self.assertRaises(OverflowError):
            ULongValue("test", 10000000000)

    # ========================================================================
    # Serialization Tests - Data Size Verification
    # ========================================================================

    def test_long_value_serializes_as_4_bytes(self):
        """LongValue must serialize as 4 bytes (int32)."""
        lv = LongValue("test", 12345)
        # Check internal data size
        self.assertEqual(len(lv._data), 4)

    def test_ulong_value_serializes_as_4_bytes(self):
        """ULongValue must serialize as 4 bytes (uint32)."""
        ulv = ULongValue("test", 12345)
        # Check internal data size
        self.assertEqual(len(ulv._data), 4)

    def test_long_value_from_data_roundtrip(self):
        """LongValue should roundtrip correctly through binary data."""
        original = LongValue("test", -12345)
        data = original._data
        restored = LongValue.from_data("test", data)
        self.assertEqual(restored.to_long(), -12345)

    def test_ulong_value_from_data_roundtrip(self):
        """ULongValue should roundtrip correctly through binary data."""
        original = ULongValue("test", 12345)
        data = original._data
        restored = ULongValue.from_data("test", data)
        self.assertEqual(restored.to_ulong(), 12345)

    # ========================================================================
    # Cross-Type Compatibility Tests
    # ========================================================================

    def test_long_value_compatible_with_llong_value(self):
        """LongValue should be safely convertible to LLongValue."""
        lv = LongValue("test", 12345)
        llv = LLongValue("test2", lv.to_long())
        self.assertEqual(llv.to_llong(), 12345)

    def test_ulong_value_compatible_with_ullong_value(self):
        """ULongValue should be safely convertible to ULLongValue."""
        ulv = ULongValue("test", 12345)
        ullv = ULLongValue("test2", ulv.to_ulong())
        self.assertEqual(ullv.to_ullong(), 12345)

    # ========================================================================
    # Error Message Validation Tests
    # ========================================================================

    def test_long_value_error_message_is_descriptive(self):
        """LongValue error message should be descriptive."""
        with self.assertRaises(OverflowError) as cm:
            LongValue("test", 5000000000)
        msg = str(cm.exception)
        self.assertIn("LongValue", msg)
        self.assertIn("32-bit", msg)
        self.assertIn("LLongValue", msg)
        self.assertIn("5000000000", msg)

    def test_ulong_value_error_message_is_descriptive(self):
        """ULongValue error message should be descriptive."""
        with self.assertRaises(OverflowError) as cm:
            ULongValue("test", 10000000000)
        msg = str(cm.exception)
        self.assertIn("ULongValue", msg)
        self.assertIn("32-bit", msg)
        self.assertIn("ULLongValue", msg)
        self.assertIn("10000000000", msg)

    # ========================================================================
    # Platform Independence Tests
    # ========================================================================

    def test_long_value_constants_are_correct(self):
        """Verify range constants match int32 limits."""
        self.assertEqual(LongValue.INT32_MIN, -(2**31))
        self.assertEqual(LongValue.INT32_MAX, 2**31 - 1)

    def test_ulong_value_constants_are_correct(self):
        """Verify range constants match uint32 limits."""
        self.assertEqual(ULongValue.UINT32_MAX, 2**32 - 1)

    def test_long_value_uses_little_endian(self):
        """LongValue should use little-endian byte order."""
        lv = LongValue("test", 0x12345678)
        # Little-endian: least significant byte first
        expected = struct.pack("<i", 0x12345678)
        self.assertEqual(lv._data, expected)

    def test_ulong_value_uses_little_endian(self):
        """ULongValue should use little-endian byte order."""
        ulv = ULongValue("test", 0x12345678)
        # Little-endian: least significant byte first
        expected = struct.pack("<I", 0x12345678)
        self.assertEqual(ulv._data, expected)

    # ========================================================================
    # String Conversion Tests
    # ========================================================================

    def test_long_value_from_string_valid(self):
        """LongValue.from_string should work with valid strings."""
        lv = LongValue.from_string("test", "12345")
        self.assertEqual(lv.to_long(), 12345)

    def test_long_value_from_string_rejects_overflow(self):
        """LongValue.from_string should reject overflow values."""
        with self.assertRaises(OverflowError):
            LongValue.from_string("test", "5000000000")

    def test_ulong_value_from_string_valid(self):
        """ULongValue.from_string should work with valid strings."""
        ulv = ULongValue.from_string("test", "12345")
        self.assertEqual(ulv.to_ulong(), 12345)

    def test_ulong_value_from_string_rejects_overflow(self):
        """ULongValue.from_string should reject overflow values."""
        with self.assertRaises(OverflowError):
            ULongValue.from_string("test", "10000000000")


if __name__ == "__main__":
    unittest.main()
