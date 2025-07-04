import json
import asyncio
import websockets
import aiohttp
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("WebSocket connection accepted")
        
        # Check market status first
        await self.check_market_status()
        
        # Start the Finnhub WebSocket connection
        self.finnhub_task = asyncio.create_task(self.connect_to_finnhub())
    
    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected with code: {close_code}")
        # Cancel the Finnhub WebSocket task
        if hasattr(self, 'finnhub_task'):
            self.finnhub_task.cancel()
    
    async def check_market_status(self):
        """Check if NASDAQ market is open"""
        try:
            url = "https://finnhub.io/api/v1/stock/market-status?exchange=US&token=d1jl9lhr01qvg5gv8gk0d1jl9lhr01qvg5gv8gkg"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Market status: {data}")
                        
                        # Send market status to client
                        await self.send(text_data=json.dumps({
                            'type': 'market_status',
                            'data': data
                        }))
                    else:
                        logger.error(f"Failed to get market status: {response.status}")
                        await self.send(text_data=json.dumps({
                            'type': 'error',
                            'message': 'Failed to check market status'
                        }))
        except Exception as e:
            logger.error(f"Error checking market status: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Market status check failed: {str(e)}'
            }))
    
    async def connect_to_finnhub(self):
        uri = "wss://ws.finnhub.io?token=d1jl9lhr01qvg5gv8gk0d1jl9lhr01qvg5gv8gkg"
        
        try:
            logger.info("Connecting to Finnhub WebSocket...")
            async with websockets.connect(uri) as websocket:
                logger.info("Connected to Finnhub WebSocket")
                
                # Subscribe to NASDAQ symbols
                symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META']
                for symbol in symbols:
                    subscribe_msg = json.dumps({'type': 'subscribe', 'symbol': symbol})
                    await websocket.send(subscribe_msg)
                    logger.info(f"Subscribed to {symbol}")
                
                # Listen for messages
                async for message in websocket:
                    try:
                        data = json.loads(message)
                        logger.info(f"Received from Finnhub: {data}")
                        
                        if data.get('type') == 'trade':
                            # Forward trade data to the client
                            await self.send(text_data=json.dumps({
                                'type': 'trade_update',
                                'data': data
                            }))
                        elif data.get('type') == 'ping':
                            # Respond to ping
                            await websocket.send(json.dumps({'type': 'pong'}))
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON decode error: {e}")
                        
        except websockets.exceptions.ConnectionClosed as e:
            logger.error(f"Finnhub WebSocket connection closed: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Connection to Finnhub closed'
            }))
        except Exception as e:
            logger.error(f"Error connecting to Finnhub: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Connection error: {str(e)}'
            }))