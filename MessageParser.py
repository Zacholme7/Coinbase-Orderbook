from OrderBook import Order

class MessageParser:
    """
    A MessageParser is an object that is used to parse incoming order messages
    """
    def __call__(self, message):
        """
        Special method used so that you can direclty call the object on messages
        
        Example usage:
            mp = MessageParser()
            parsedMessage = mp(message)

        :param message: message receieved from the websocket that is to be parsed
        """
        # extract the type for matching
        orderType = message["type"]
        
        # dispatch to proper parse method
        if orderType == "open":
            return self.parseOpen(message)
        elif orderType == "done":
            return self.parseDone(message)
        elif orderType == "change":
            return self.parseChange(message)
        elif orderType == "match":
            return self.parseMatch(message)
        else:
            return None

    def parseOpen(self, message):
        """
        parses a message of type "open"

        :param message: the open message to be parsed
        """
        orderId = message["order_id"]
        orderPrice = float(message["price"])
        orderSize = float(message["remaining_size"])
        orderSide = 0 if message["side"] == "sell" else 1
        orderSeq = int(message["sequence"])
        return Order("open", orderId, orderPrice, orderSize, orderSide, orderSeq)

    def parseDone(self, message):
        """
        parses a message of type "done"

        :param message: the done message to be parsed
        """
        orderId = message["order_id"]
        # deal with case where done message is sent without price
        if "price" in message:
            orderPrice = float(message["price"])
        else:
            return None
        orderSize = float(message["remaining_size"])
        orderSide = 0 if message["side"] == "sell" else 1
        orderSeq = int(message["sequence"])
        return Order("done", orderId, orderPrice, orderSize, orderSide, orderSeq)

    def parseChange(self, message):
        """
        parses a message of type "change"

        :param message: the change message to be parsed
        """
        orderId = message["order_id"]
        orderReason = message["reason"]
        orderSize = float(message["new_size"])

        # differentiate between STP and price change
        if orderReason == "STP":
            orderPrice = float(message["price"])
        else:
            orderPrice = float(message["new_price"])

        orderSide = 0 if message["side"] == "sell" else 1
        orderSeq = int(message["sequence"])
        return Order("change", orderId, orderPrice, orderSize, orderSide, orderSeq)

    def parseMatch(self, message):
        """
        parses a message of type "match"

        :param message: the match message to be parsed
        """
        orderId = message["maker_order_id"]
        orderPrice = float(message["price"])
        orderSize = float(message["size"])
        orderSide = 0 if message["side"] == "sell" else 1
        orderSeq = int(message["sequence"])
        return Order("match", orderId, orderPrice, orderSize, orderSide, orderSeq)




