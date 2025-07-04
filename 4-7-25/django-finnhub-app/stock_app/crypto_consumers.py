import json
import asyncio
import websockets
import aiohttp
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class CryptoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("Crypto WebSocket connection accepted")
        
        # Check crypto market status (crypto markets are generally 24/7)
        await self.check_crypto_market_status()
        
        # Start the Finnhub WebSocket connection
        self.finnhub_task = asyncio.create_task(self.connect_to_finnhub())
    
    async def disconnect(self, close_code):
        logger.info(f"Crypto WebSocket disconnected with code: {close_code}")
        # Cancel the Finnhub WebSocket task
        if hasattr(self, 'finnhub_task'):
            self.finnhub_task.cancel()
    
    async def check_crypto_market_status(self):
        """Check crypto market status (usually 24/7)"""
        try:
            # Crypto markets are generally 24/7, so we'll send a default open status
            market_data = {
                'isOpen': True,
                'exchange': 'Binance',
                'timezone': 'UTC',
                'session': 'Regular'
            }
            
            logger.info(f"Crypto market status: {market_data}")
            
            # Send market status to client
            await self.send(text_data=json.dumps({
                'type': 'market_status',
                'data': market_data
            }))
        except Exception as e:
            logger.error(f"Error checking crypto market status: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Crypto market status check failed: {str(e)}'
            }))
    
    async def connect_to_finnhub(self):
        uri = "wss://ws.finnhub.io?token=d1jl9lhr01qvg5gv8gk0d1jl9lhr01qvg5gv8gkg"
        
        try:
            logger.info("Connecting to Finnhub WebSocket for crypto...")
            async with websockets.connect(uri) as websocket:
                logger.info("Connected to Finnhub WebSocket for crypto")
                
                # Subscribe to Binance crypto symbols
                crypto_symbols = [
                    'BINANCE:BTCUSDT',
                    'BINANCE:ETHUSDT',
                    'BINANCE:BNBUSDT',
                    'BINANCE:XRPUSDT',
                    'BINANCE:ADAUSDT',
                    'BINANCE:SOLUSDT',
                    'BINANCE:MATICUSDT',
                    'BINANCE:DOGEUSDT',
                    'BINANCE:DOTUSDT',
                    'BINANCE:AVAXUSDT'
                ]
                
                for symbol in crypto_symbols:
                    subscribe_msg = json.dumps({'type': 'subscribe', 'symbol': symbol})
                    await websocket.send(subscribe_msg)
                    logger.info(f"Subscribed to {symbol}")
                
                # Listen for messages
                async for message in websocket:
                    try:
                        data = json.loads(message)
                        logger.info(f"Received from Finnhub crypto: {data}")
                        
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
            logger.error(f"Finnhub crypto WebSocket connection closed: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Connection to Finnhub closed'
            }))
        except Exception as e:
            logger.error(f"Error connecting to Finnhub crypto: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Connection error: {str(e)}'
            }))