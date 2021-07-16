import unittest
import mini_st

class TestTransactionQuery(unittest.TestCase):
    def test_map_values_to_dict(self):
        test_values = {
            "field_0": "sitereference (Alpha 20 char)",
            "value_0": "asite12345"
        }
        expected = {
            "sitereference": [{"value": "asite12345"}]
        }
        self.assertEqual(mini_st.map_values_to_dict(test_values), expected)

if __name__ == "__main__":
    unittest.main()