import unittest
import pandas as pd
import numpy as np
from nowtrade import criteria_group, strategy
from nowtrade.action import Long, Short, LongExit, ShortExit
from testing_data import DummyCriteria, msft_data

class TestCriteriaGroup(unittest.TestCase):
    def test_criteria_group(self):
        criteria_list = [DummyCriteria(True), DummyCriteria(True)]
        with self.assertRaises(criteria_group.InvalidAction):
            cg = criteria_group.CriteriaGroup(criteria_list, 'INVALID', 'MSFT')
        cg = criteria_group.CriteriaGroup(criteria_list, Long(), 'MSFT')
        self.assertEquals(str(cg), 'CriteriaGroup(criteria_list=[DummyCriteria(), DummyCriteria(), Not_InMarket(symbol=MSFT)], action=long, symbol=MSFT)')
        self.assertEqual(cg._action, 1)
        out = cg.get_result(msft_data)
        self.assertEqual(len(cg.criteria_list), 3) # One extra: NotInMarket
        self.assertEqual(out, strategy.LONG)
        criteria_list = [DummyCriteria(True), DummyCriteria(False)]
        cg = criteria_group.CriteriaGroup(criteria_list, Long(), 'MSFT')
        out = cg.get_result(msft_data)
        self.assertEqual(out, strategy.NO_ACTION)

if __name__ == "__main__":
    unittest.main()
