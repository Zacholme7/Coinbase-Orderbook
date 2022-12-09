# dummy orders used for testing in TestOrderBook and TestMessageParser
openOrder1 = {
  "type": "open",
  "time": "2014-11-07T08:19:27.028459Z",
  "product_id": "BTC-USD",
  "sequence": 10,
  "order_id": "order1",
  "price": "200.2",
  "remaining_size": "1.00",
  "side": "sell"
}

openOrder2 = {
  "type": "open",
  "time": "2014-11-07T08:19:27.028459Z",
  "product_id": "BTC-USD",
  "sequence": 10,
  "order_id": "order2",
  "price": "200.2",
  "remaining_size": "1.00",
  "side": "sell"
}

openOrder3 = {
  "type": "open",
  "time": "2014-11-07T08:19:27.028459Z",
  "product_id": "BTC-USD",
  "sequence": 10,
  "order_id": "order3",
  "price": "200.2",
  "remaining_size": "1.00",
  "side": "sell"
}

doneOrder1 = {
  "type": "done",
  "time": "2014-11-07T08:19:27.028459Z",
  "product_id": "BTC-USD",
  "sequence": 10,
  "price": "200.2",
  "order_id": "order1",
  "reason": "filled",
  "side": "sell",
  "remaining_size": "0"
}

doneOrder2 = {
  "type": "done",
  "time": "2014-11-07T08:19:27.028459Z",
  "product_id": "BTC-USD",
  "sequence": 10,
  "price": "200.2",
  "order_id": "order2",
  "reason": "filled",
  "side": "sell",
  "remaining_size": "0"
}

doneOrder3 = {
  "type": "done",
  "time": "2014-11-07T08:19:27.028459Z",
  "product_id": "BTC-USD",
  "sequence": 10,
  "price": "200.2",
  "order_id": "order3",
  "reason": "filled",
  "side": "sell",
  "remaining_size": "0"
}

changeOrder1 = {
  "type": "change",
  "reason":"STP",
  "time": "2014-11-07T08:19:27.028459Z",
  "sequence": 80,
  "order_id": "order1",
  "side": "sell",
  "product_id": "BTC-USD",
  "old_size": "1.0",
  "new_size": "0.5",
  "price": "200.2"
}

changeOrder2 = {
  "type": "change",
  "reason":"modify_order",
  "time": "2022-06-06T22:55:43.433114Z",
  "sequence": 24753,
  "order_id": "order2",
  "side": "sell",
  "product_id": "ETH-USD",
  "old_size": "1",
  "new_size": "0.5",
  "old_price": "200.2",
  "new_price": "100.2"
}

matchOrder1 = {
  "type": "match",
  "trade_id": 10,
  "sequence": 50,
  "maker_order_id": "order1",
  "taker_order_id": "foo",
  "time": "2014-11-07T08:19:27.028459Z",
  "product_id": "BTC-USD",
  "size": "0.75",
  "price": "200.2",
  "side": "sell"
}
