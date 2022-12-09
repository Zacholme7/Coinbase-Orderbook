from DummyOrders import openOrder1, openOrder2, openOrder3, doneOrder1, doneOrder2, doneOrder3, changeOrder1, changeOrder2, matchOrder1
import unittest
#---------------
# quick hack to import from parent
import sys
sys.path.append("../")
#---------------
from OrderBook import OrderBook
from MessageParser import MessageParser

mp = MessageParser()

class TestClass(unittest.TestCase):
    def testAdd(self):
        ob = OrderBook()
        #                  head                  tail
        # 200.2: None <-> order1 <-> order2 <-> order3 <-> None
        ob.processMessage(mp(openOrder1))
        ob.processMessage(mp(openOrder2))
        ob.processMessage(mp(openOrder3))

        # get the limit to access the orders
        limit = ob.askLimits[200.2]

        # test head
        head = limit.head
        self.assertEqual(head.id, "order1")
        self.assertEqual(head.prev, None)
        self.assertEqual(head.next.id, "order2")

        # test middle
        middle = limit.head.next
        self.assertEqual(middle.id, "order2")
        self.assertEqual(middle.prev.id, "order1")
        self.assertEqual(middle.next.id, "order3")

        # test tail
        tail = limit.tail
        self.assertEqual(tail.id, "order3")
        self.assertEqual(tail.prev.id, "order2")
        self.assertEqual(tail.next, None)

    def testDone(self):
        ob = OrderBook()
        #                  head                  tail
        # 200.2: None <-> order1 <-> order2 <-> order3 <-> None
        ob.processMessage(mp(openOrder1))
        ob.processMessage(mp(openOrder2))
        ob.processMessage(mp(openOrder3))

        # get the limit to access the orders
        limit = ob.askLimits[200.2]

        # remove middle
        ob.processMessage(mp(doneOrder2))
        self.assertEqual(limit.head.next.id, "order3")
        self.assertEqual(limit.tail.prev.id, "order1")

        # remove head 
        ob.processMessage(mp(doneOrder1))
        self.assertEqual(limit.head.id, "order3")
        self.assertEqual(limit.tail.id, "order3")

        # remove head/tail (last item on order)
        ob.processMessage(mp(doneOrder3))
        self.assertEqual(limit.head, None)
        self.assertEqual(limit.tail, None)

    def testChange(self):
        ob = OrderBook()
        #                  head                  tail
        # 200.2: None <-> order1 <-> order2 <-> order3 <-> None
        ob.processMessage(mp(openOrder1))
        ob.processMessage(mp(openOrder2))
        ob.processMessage(mp(openOrder3))

        # get the limit to access the orders
        limit = ob.askLimits[200.2]

        # this should remove order1 from the head, set it to the tail, and change its size
        ob.processMessage(mp(changeOrder1))
        self.assertEqual(limit.tail.id, "order1")
        self.assertEqual(limit.tail.quantity, 0.5)
        self.assertEqual(limit.head.id, "order2")

        # this should remove order2 from the head and create a new limit 
        # where this is the only object
        self.assertEqual(len(ob.askLimits), 1)
        ob.processMessage(mp(changeOrder2))
        self.assertEqual(len(ob.askLimits), 2)

        newLimit = ob.askLimits[100.2]
        self.assertEqual(newLimit.head.id, "order2")
        self.assertEqual(newLimit.head.quantity, 0.5)
        self.assertEqual(newLimit.head.price, 100.2)
        self.assertEqual(limit.head.id, "order3")
        self.assertEqual(limit.tail.id, "order1")

    def testMatch(self):
        ob = OrderBook()
        #                  head                  tail
        # 200.2: None <-> order1 <-> order2 <-> order3 <-> None
        ob.processMessage(mp(openOrder1))
        ob.processMessage(mp(openOrder2))
        ob.processMessage(mp(openOrder3))

        # get the limit to access the orders
        limit = ob.askLimits[200.2]

        # match against order 1, size should be adjusted to .25
        ob.processMessage(mp(matchOrder1))
        self.assertEqual(limit.head.quantity, .25)

if __name__ == "__main__":
    unittest.main()















