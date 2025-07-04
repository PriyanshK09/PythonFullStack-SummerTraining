class CryptoWebSocket {
    constructor() {
        this.socket = null;
        this.reconnectInterval = 5000;
        this.cryptoPrices = {};
        this.isMarketOpen = true; // Crypto markets are generally 24/7
        this.connect();
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/crypto/`;
        
        console.log('Connecting to crypto WebSocket:', wsUrl);
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = (event) => {
            console.log('Connected to crypto WebSocket');
            this.updateConnectionStatus('Connected', 'connected');
        };
        
        this.socket.onmessage = (event) => {
            console.log('Received crypto message:', event.data);
            try {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            } catch (error) {
                console.error('Error parsing crypto message:', error);
            }
        };
        
        this.socket.onclose = (event) => {
            console.log('Crypto WebSocket connection closed:', event);
            this.updateConnectionStatus('Disconnected', 'disconnected');
            this.reconnect();
        };
        
        this.socket.onerror = (error) => {
            console.error('Crypto WebSocket error:', error);
            this.updateConnectionStatus('Connection Error', 'disconnected');
        };
    }

    handleMessage(data) {
        console.log('Handling crypto message:', data);
        
        if (data.type === 'market_status') {
            this.handleMarketStatus(data.data);
        } else if (data.type === 'trade_update' && data.data) {
            if (data.data.type === 'trade' && data.data.data) {
                const trades = data.data.data;
                console.log('Processing crypto trades:', trades);
                trades.forEach(trade => {
                    console.log('Updating crypto:', trade.s, 'Price:', trade.p);
                    this.updateCryptoPrice(trade.s, trade.p, trade.t);
                });
            }
        } else if (data.type === 'error') {
            console.error('Crypto server error:', data.message);
            this.updateConnectionStatus('Error: ' + data.message, 'disconnected');
        }
    }

    handleMarketStatus(marketData) {
        console.log('Crypto market status:', marketData);
        this.isMarketOpen = marketData.isOpen;
        
        if (this.isMarketOpen) {
            this.updateConnectionStatus('Market Open - 24/7', 'connected');
        }
    }

    updateCryptoPrice(symbol, price, timestamp) {
        console.log(`Updating crypto ${symbol} with price ${price}`);
        const cryptoCard = document.getElementById(symbol);
        if (!cryptoCard) {
            console.warn(`No crypto card found for symbol: ${symbol}`);
            return;
        }

        const priceElement = cryptoCard.querySelector('.price');
        const changeElement = cryptoCard.querySelector('.change');
        const timestampElement = cryptoCard.querySelector('.timestamp');

        if (!priceElement || !changeElement || !timestampElement) {
            console.warn(`Missing elements in crypto card for ${symbol}`);
            return;
        }

        // Store previous price for change calculation
        const previousPrice = this.cryptoPrices[symbol] || price;
        this.cryptoPrices[symbol] = price;

        // Format price based on crypto value
        let formattedPrice;
        if (price >= 1000) {
            formattedPrice = `$${price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        } else if (price >= 1) {
            formattedPrice = `$${price.toFixed(4)}`;
        } else {
            formattedPrice = `$${price.toFixed(6)}`;
        }

        // Update price
        priceElement.textContent = formattedPrice;
        
        // Calculate and update change
        const change = price - previousPrice;
        const changePercent = previousPrice ? ((change / previousPrice) * 100) : 0;
        
        let formattedChange;
        if (Math.abs(change) >= 1) {
            formattedChange = change.toFixed(2);
        } else {
            formattedChange = change.toFixed(6);
        }
        
        if (change > 0) {
            changeElement.textContent = `+$${formattedChange} (+${changePercent.toFixed(2)}%)`;
            changeElement.className = 'change positive';
        } else if (change < 0) {
            changeElement.textContent = `$${formattedChange} (${changePercent.toFixed(2)}%)`;
            changeElement.className = 'change negative';
        } else {
            changeElement.textContent = `$0.00 (0.00%)`;
            changeElement.className = 'change';
        }

        // Update timestamp
        const date = new Date(timestamp);
        timestampElement.textContent = `Last updated: ${date.toLocaleTimeString()}`;

        // Add pulse animation
        cryptoCard.classList.add('pulse');
        setTimeout(() => {
            cryptoCard.classList.remove('pulse');
        }, 1000);
        
        console.log(`Successfully updated crypto ${symbol}`);
    }

    updateConnectionStatus(message, className) {
        const statusElement = document.getElementById('connection-status');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `status ${className}`;
        }
    }

    reconnect() {
        setTimeout(() => {
            console.log('Attempting to reconnect to crypto WebSocket...');
            this.updateConnectionStatus('Reconnecting...', '');
            this.connect();
        }, this.reconnectInterval);
    }
}

// Initialize crypto WebSocket connection when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing crypto WebSocket...');
    new CryptoWebSocket();
});