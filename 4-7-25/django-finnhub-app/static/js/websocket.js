class StockWebSocket {
    constructor() {
        this.socket = null;
        this.reconnectInterval = 5000;
        this.stockPrices = {};
        this.isMarketOpen = false;
        this.connect();
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/stock/`;
        
        console.log('Connecting to:', wsUrl);
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = (event) => {
            console.log('Connected to WebSocket');
            this.updateConnectionStatus('Connected', 'connected');
        };
        
        this.socket.onmessage = (event) => {
            console.log('Received message:', event.data);
            try {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            } catch (error) {
                console.error('Error parsing message:', error);
            }
        };
        
        this.socket.onclose = (event) => {
            console.log('WebSocket connection closed:', event);
            this.updateConnectionStatus('Disconnected', 'disconnected');
            this.reconnect();
        };
        
        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus('Connection Error', 'disconnected');
        };
    }

    handleMessage(data) {
        console.log('Handling message:', data);
        
        if (data.type === 'market_status') {
            this.handleMarketStatus(data.data);
        } else if (data.type === 'trade_update' && data.data) {
            if (data.data.type === 'trade' && data.data.data) {
                const trades = data.data.data;
                console.log('Processing trades:', trades);
                trades.forEach(trade => {
                    console.log('Updating stock:', trade.s, 'Price:', trade.p);
                    this.updateStockPrice(trade.s, trade.p, trade.t);
                });
            }
        } else if (data.type === 'error') {
            console.error('Server error:', data.message);
            this.updateConnectionStatus('Error: ' + data.message, 'disconnected');
        }
    }

    handleMarketStatus(marketData) {
        console.log('Market status:', marketData);
        
        // Check if market is open
        this.isMarketOpen = marketData.isOpen;
        
        if (!this.isMarketOpen) {
            this.showMarketClosedMessage(marketData);
        }
    }

    showMarketClosedMessage(marketData) {
        // Update connection status
        this.updateConnectionStatus('Market Closed', 'market-closed');
        
        // Show market closed overlay
        this.createMarketClosedOverlay(marketData);
        
        // Hide stock prices
        this.hideStockPrices();
    }

    createMarketClosedOverlay(marketData) {
        // Remove existing overlay if present
        const existingOverlay = document.getElementById('market-closed-overlay');
        if (existingOverlay) {
            existingOverlay.remove();
        }

        // Create overlay
        const overlay = document.createElement('div');
        overlay.id = 'market-closed-overlay';
        overlay.className = 'market-closed-overlay';
        
        // Get IST time
        const istTime = new Date().toLocaleString('en-IN', {
            timeZone: 'Asia/Kolkata',
            hour12: true,
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric'
        });

        overlay.innerHTML = `
            <div class="market-closed-content">
                <button class="close-button" onclick="this.closest('.market-closed-overlay').remove()">×</button>
                <div class="market-closed-icon">🕒</div>
                <h2>NASDAQ Market is Currently Closed</h2>
                <div class="market-info">
                    <p><strong>Current IST Time:</strong> ${istTime}</p>
                    <p><strong>Market Status:</strong> ${this.isMarketOpen ? 'Open' : 'Closed'}</p>
                    <p><strong>Exchange:</strong> US (NASDAQ)</p>
                </div>
                <div class="market-schedule">
                    <h3>📅 Market Schedule (IST)</h3>
                    <div class="schedule-grid">
                        <div class="schedule-item">
                            <span class="schedule-label">Regular Trading</span>
                            <span class="schedule-time">7:00 PM - 1:30 AM</span>
                        </div>
                        <div class="schedule-item">
                            <span class="schedule-label">Pre-Market</span>
                            <span class="schedule-time">5:30 PM - 7:00 PM</span>
                        </div>
                        <div class="schedule-item">
                            <span class="schedule-label">After Hours</span>
                            <span class="schedule-time">1:30 AM - 9:30 AM</span>
                        </div>
                        <div class="schedule-item">
                            <span class="schedule-label">Extended Hours</span>
                            <span class="schedule-time">4:00 AM - 8:00 PM</span>
                        </div>
                    </div>
                </div>
                <div class="next-session">
                    <p>💡 Live data will be available when the market opens at <strong>7:00 PM IST</strong></p>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);
        
        // Add click outside to close
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.remove();
            }
        });
        
        // Add escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && document.getElementById('market-closed-overlay')) {
                overlay.remove();
            }
        });
    }

    hideStockPrices() {
        const stockCards = document.querySelectorAll('.stock-card');
        stockCards.forEach(card => {
            card.style.opacity = '0.5';
            card.style.pointerEvents = 'none';
        });
    }

    updateStockPrice(symbol, price, timestamp) {
        if (!this.isMarketOpen) {
            console.log('Market is closed, not updating prices');
            return;
        }

        console.log(`Updating ${symbol} with price ${price}`);
        const stockCard = document.getElementById(symbol);
        if (!stockCard) {
            console.warn(`No stock card found for symbol: ${symbol}`);
            return;
        }

        const priceElement = stockCard.querySelector('.price');
        const changeElement = stockCard.querySelector('.change');
        const timestampElement = stockCard.querySelector('.timestamp');

        if (!priceElement || !changeElement || !timestampElement) {
            console.warn(`Missing elements in stock card for ${symbol}`);
            return;
        }

        // Store previous price for change calculation
        const previousPrice = this.stockPrices[symbol] || price;
        this.stockPrices[symbol] = price;

        // Update price
        priceElement.textContent = `$${price.toFixed(2)}`;
        
        // Calculate and update change
        const change = price - previousPrice;
        const changePercent = previousPrice ? ((change / previousPrice) * 100) : 0;
        
        if (change > 0) {
            changeElement.textContent = `+$${change.toFixed(2)} (+${changePercent.toFixed(2)}%)`;
            changeElement.className = 'change positive';
        } else if (change < 0) {
            changeElement.textContent = `$${change.toFixed(2)} (${changePercent.toFixed(2)}%)`;
            changeElement.className = 'change negative';
        } else {
            changeElement.textContent = `$0.00 (0.00%)`;
            changeElement.className = 'change';
        }

        // Update timestamp
        const date = new Date(timestamp);
        timestampElement.textContent = `Last updated: ${date.toLocaleTimeString()}`;

        // Add pulse animation
        stockCard.classList.add('pulse');
        setTimeout(() => {
            stockCard.classList.remove('pulse');
        }, 1000);
        
        console.log(`Successfully updated ${symbol}`);
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
            console.log('Attempting to reconnect...');
            this.updateConnectionStatus('Reconnecting...', '');
            this.connect();
        }, this.reconnectInterval);
    }
}

// Initialize WebSocket connection when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing WebSocket...');
    new StockWebSocket();
});