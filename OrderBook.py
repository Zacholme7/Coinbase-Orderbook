from sortedcontainers import SortedDict
"""
L2 orderbook that operates on a full channel data stream
Processes orders of type:
    open: a new order has been added to the order book
    done: a resting order has been canceled and should be removed from the order book
    match: a trade has occured and the size has to be updated
    change: a resting order has changed in size of price

Structure:
    An orderbook object is meant to track state and process incoming messages.
    It contains 3 dictionaries: 1 to track active orders, 1 to track the buy side,
    and 1 to track the sell side. The buy and sell side are set up identically. The
    price of a limit will be used as a key and a limit object will be stored as the value.
    Within the limit object, there is a linked list of orders which is used to facilitate 
    the matching in FIFO manner. Additionally, the Limit object will only keep track of the
    head and tail limit in the linked list to facilitate for quick insert and removal. 
"""

class Limit:
    """
    Represents a limit order at a certain price level

    Attributes:
        Price: float to represent the price of the limit
        Head: Order object that represents the next order to be filled
        Tail: Order object that represents the last order to be filled
    """
    def __init__(self, price: float):
        self.price = price
        self.head = None
        self.tail = None

class Order:
    """
    Represents each order that comes in
    Object get stored in a limit level object as a FIFO linked list

    Attributes:
        Type: a string representing the order type ["open", "done", "change", "match"]
        Identifier: a string representing the unique id for each order
        Price: a float representing the price at which Limit this Order should act upon
        Quantity: a float representing the quantity of the order or the new quantity of the order depending on the type
        Side: a int representing if an order is on the sell side (0) or the buy side (1)
        Sequence: a int representing where in the order sequence the Order was received
        Prev: None by default, updated to contain a pointer to the previous Order in the queue
        Next: None by default, updated to contain a pointer to the next Order in the queue
    """
    def __init__(self, orderType: str, identifier: str, price: float, quantity: float, side: int, sequence: int):
        self.type = orderType
        self.id = identifier
        self.price = price
        self.quantity = quantity
        self.side = side
        self.sequence = sequence
        self.prev = None
        self.next = None

class OrderBook:
    """
    Represents an Orderbook filled with Limits that each contain
    a linked list of orders

    Attributes:
        orderBook: tracks all active orders in the form of Order.id : Order Object
        askLimits: tracks all the limits on the sell side, in the form of Limit.price: Limit Object
            - Limit object then contains a linked list or orders at that level
        buyLimits: tracks all the limits on the buy side, in the form of Limit.price: Limit Object
            - Limit object then contains a linked list or orders at that level
        currSeqNum: tracks the sequence number of the current order
    """
    def __init__(self):
        self.orderBook = {}
        self.askLimits = SortedDict() 
        self.buyLimits = SortedDict() 
        self.currSeqNum = -1

    def processMessage(self, order):
        """
        processes an order by extracting the relevant attributes and dispatching it 
        to the correct processing method

        :param order: the order to be processes
        """
        # extract the relevant data
        orderType = order.type
        orderIden = order.id
        orderPrice = order.price 
        orderSize = order.quantity
        orderSide = self.askLimits if order.side == 0 else self.buyLimits

        # guard against out of order messages
        if order.sequence < self.currSeqNum:
            return
        self.currSeqNum = order.sequence

        # execute correct order
        if orderType == "open":
            self.addOrder(order, orderPrice, orderSide)
        elif orderType == "done":
            self.removeOrder(orderIden, orderPrice, orderSide)
        elif orderType == "change":
            self.changeOrder(order, orderIden, orderPrice, orderSide)
        elif orderType == "match":
            self.matchOrder(orderIden, orderSize, orderSide)

    def changeOrder(self, order, iden, price, side):
        """
        processes an order of type "change"

        :param order: the change order object 
        :param iden: the id of the order to be changed
        :param price: the changed or unchanged price of the order depending on the change reason
        :param side: reference to the side of the order (buy or ask)
        """
        # check if the order exists
        if iden in self.orderBook:
            # remove the old order
            oldOrder = self.orderBook[iden]
            self.removeOrder(iden, oldOrder.price, side);
            self.addOrder(order, price, side)

    def matchOrder(self, makerId, size, side):
        """
        processes an order of type "match"

        :param order: the match order object 
        :param makerId: the id of the order maker
        :param size: the size of the match order that is to be executed
        :param side: reference to the side of the order (buy or ask)
        """
        # check if the order exists
        if makerId in self.orderBook:

            # if it exists, get the limit object
            orderToAdjust = self.orderBook[makerId]

            # update the order size
            originalSize = orderToAdjust.quantity
            newSize = originalSize - size

            # if the order is filled, just remove it right away
            # else update quantity
            if newSize <= 0:
                self.removeOrder(orderToAdjust.id, orderToAdjust.price, side)
            else:
                orderToAdjust.quantity = newSize

            # output the top bid/ask prices
            self.outputBidAsk()

    def addOrder(self, order, price, side):
        """
        processes an order of type "add"

        :param order: the add order object
        :param price: the price at which the object corresponds to and is to be added at
        :param side: reference to the side of the order (buy or ask)
        """
        
        if price in side: 
            # add the order to an existing limit level
            limit = side[price]
            if limit.head == None and limit.tail == None:
                limit.head = order
                limit.tail = order
            else:
                tmpTail = limit.tail
                tmpTail.next = order
                order.prev = tmpTail
                limit.tail = order
        else:  
            # make a new limit level and add the order in
            limit = Limit(order.price)
            side[price] = limit
            limit.head = order
            limit.tail = order

        # order is now active, add it to orderbook
        self.orderBook[order.id] = order

    def removeOrder(self, iden, price, side):
        """
        processes an order of type "remove"

        :param iden: the id of the order to be removed
        :param price: the price at which the object corresponds to and is to be added at
        :param side: reference to the side of the order (buy or ask)
        """
        # if there is a limit open and the order is in the orderbook, proceed
        if price in side and iden in self.orderBook:
            limit = side[price]
            order = self.orderBook[iden]
            
            # guard against case where a limit with a single order was previously
            # removed by a match
            if limit.head == None or limit.tail == None:
                del self.orderBook[order.id]
                return

            # adjust the head and tail pointers of the limit if necessary
            if limit.head.id == order.id and limit.tail.id == order.id:
                limit.head = None
                limit.tail = None
            elif limit.head.id == order.id:
                limit.head = order.next
            elif limit.tail.id == order.id:
                limit.tail = order.prev

            # remove the order from the order list
            if order.prev != None and order.next != None:
                order.prev.next =  order.next
                order.next.prev = order.prev
            elif order.next != None:
                order.next.prev = None
                order.next = None
            elif order.prev != None:
                order.prev.next = None
                order.prev = None

            # remove the order out of the active orders
            del self.orderBook[order.id]

    def outputBidAsk(self):
        """
        outputs the top 5 bid and ask prices 
        called after each match order is processed
        """
        i = 0
        bestAsks = []
        print("Best Asks")
        for limit in self.askLimits:
            topOrder = self.askLimits[limit]
            if topOrder.head != None:
                bestAsks.append((topOrder.head.quantity, topOrder.head.price))
                i += 1
                if i == 5: break
        for ele in reversed(bestAsks):
            print(f"{ele[0]: <.5f} @ {ele[1]: <.2f}")
        print("-----------------------------")
        i = 0
        for limit in reversed(self.buyLimits):
            topOrder = self.buyLimits[limit]
            if topOrder.head != None:
                print(f"{topOrder.head.quantity: <.5f} @ {topOrder.head.price: <.2f}")
                i += 1
                if i == 5: break
        print("Best Bids")
        print("\n")








