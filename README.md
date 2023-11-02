# Real-Time Order Book Implementation

## Overview
This Python application is a real-time order book implementation for tracking cryptocurrency trading orders from the Coinbase exchange. It uses WebSockets for live data feed and processes different types of messages such as open, done, match, and change.

## How It Works
The order book listens to a WebSocket feed and updates its state based on the messages received. It maintains a sorted list of buy and sell orders and can output the current top bids and asks.

## Features
- Real-time connection to Coinbase exchange via WebSocket.
- Handling of `open`, `done`, `match`, and `change` order messages.
- Dynamic order processing with FIFO matching logic.
- Output of top 5 bid and ask prices after each match.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.x installed.
- `websockets` library installed.
- `asyncio` for asynchronous event handling.
- `json` for JSON manipulation.

## Installation
To install the Real-Time Order Book, follow these steps:
git clone https://github.com/your-github-username/order-book.git
cd order-book
pip install websockets asyncio

## Usage
To run the order book, execute the main script:
python main.py
