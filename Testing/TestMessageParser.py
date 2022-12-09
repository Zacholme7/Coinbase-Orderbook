from DummyOrders import openOrder1, doneOrder1, changeOrder1, changeOrder2, matchOrder1
import unittest
#---------------
# quick hack to import from parent
import sys
sys.path.append("../")
#---------------
from MessageParser import MessageParser

mp = MessageParser()

class TestClass(unittest.TestCase):
    def testParseOpen(self):
        openOrder = mp(openOrder1) 
        self.assertEqual(openOrder.type,    "open")
        self.assertEqual(openOrder.id,      "order1")
        self.assertEqual(openOrder.price,    200.2)
        self.assertEqual(openOrder.quantity, 1.00)
        self.assertEqual(openOrder.side,     0)
        self.assertEqual(openOrder.sequence, 10)

    def testParseDone(self):
        doneOrder = mp(doneOrder1) 
        self.assertEqual(doneOrder.type,    "done")
        self.assertEqual(doneOrder.id,      "order1")
        self.assertEqual(doneOrder.price,    200.2)
        self.assertEqual(doneOrder.quantity, 0)
        self.assertEqual(doneOrder.side,     0)
        self.assertEqual(doneOrder.sequence, 10)

    def testParseChange(self):
        changeOrderQty = mp(changeOrder1)
        self.assertEqual(changeOrderQty.type,    "change")
        self.assertEqual(changeOrderQty.id,      "order1")
        self.assertEqual(changeOrderQty.price,    200.2)
        self.assertEqual(changeOrderQty.quantity, 0.5)
        self.assertEqual(changeOrderQty.side,     0)
        self.assertEqual(changeOrderQty.sequence, 80)

        changeOrderPrice = mp(changeOrder2)
        self.assertEqual(changeOrderPrice.type,    "change")
        self.assertEqual(changeOrderPrice.id,      "order2")
        self.assertEqual(changeOrderPrice.price,    100.2)
        self.assertEqual(changeOrderPrice.quantity, 0.5)
        self.assertEqual(changeOrderPrice.side,     0)
        self.assertEqual(changeOrderPrice.sequence, 24753)

    def testParseMatch(self):
        matchOrder = mp(matchOrder1)
        self.assertEqual(matchOrder.type,    "match")
        self.assertEqual(matchOrder.id,      "order1")
        self.assertEqual(matchOrder.price,    200.2)
        self.assertEqual(matchOrder.quantity, 0.75)
        self.assertEqual(matchOrder.side,     0)
        self.assertEqual(matchOrder.sequence, 50)

if __name__ == "__main__":
    unittest.main()
