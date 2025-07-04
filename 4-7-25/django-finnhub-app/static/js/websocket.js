class StockWebSocket {
    constructor() {
        this.socket = null;
        this.reconnectInterval = 5000;
        this.stockPrices = {};
        this.isMarketOpen = false;
        this.connect();
        this.setupCompanyClickHandlers();
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

    setupCompanyClickHandlers() {
        // Add click handlers to company names
        document.querySelectorAll('.stock-card h3').forEach(header => {
            header.addEventListener('click', (e) => {
                e.stopPropagation(); // Prevent event bubbling
                const stockCard = e.target.closest('.stock-card');
                const symbol = stockCard.id;
                this.showCompanyProfile(symbol);
            });
            
            // Ensure header stays clickable even when card is disabled
            header.style.pointerEvents = 'auto';
            header.style.cursor = 'pointer';
        });
    }

    async showCompanyProfile(symbol) {
        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'company-profile-overlay';
        overlay.innerHTML = `
            <div class="company-profile-content">
                <button class="close-button" onclick="this.closest('.company-profile-overlay').remove()">×</button>
                <div class="loading-spinner">
                    <div class="spinner"></div>
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
        const escapeHandler = (e) => {
            if (e.key === 'Escape' && document.querySelector('.company-profile-overlay')) {
                overlay.remove();
                document.removeEventListener('keydown', escapeHandler);
            }
        };
        document.addEventListener('keydown', escapeHandler);

        // Fetch company data
        try {
            const response = await fetch(`https://finnhub.io/api/v1/stock/profile2?symbol=${symbol}&token=d1jl9lhr01qvg5gv8gk0d1jl9lhr01qvg5gv8gkg`);
            const data = await response.json();
            
            if (response.ok && data.name) {
                this.renderCompanyProfile(overlay, data, symbol);
            } else {
                this.renderErrorMessage(overlay, 'Company profile not found');
            }
        } catch (error) {
            console.error('Error fetching company profile:', error);
            this.renderErrorMessage(overlay, 'Failed to load company profile');
        }
    }

    renderCompanyProfile(overlay, data, symbol) {
        const content = overlay.querySelector('.company-profile-content');
        
        // Format market cap
        const formatMarketCap = (value) => {
            if (value >= 1e12) return `$${(value / 1e12).toFixed(2)}T`;
            if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
            if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`;
            return `$${value?.toLocaleString() || 'N/A'}`;
        };

        // Format employee count
        const formatEmployees = (count) => {
            if (count >= 1e6) return `${(count / 1e6).toFixed(1)}M`;
            if (count >= 1e3) return `${(count / 1e3).toFixed(1)}K`;
            return count?.toLocaleString() || 'N/A';
        };

        content.innerHTML = `
            <button class="close-button" onclick="this.closest('.company-profile-overlay').remove()">×</button>
            
            <div class="company-header">
                <img src="${data.logo}" alt="${data.name} logo" class="company-logo" onerror="this.style.display='none'">
                <div class="company-title">
                    <h2 class="company-name">${data.name}</h2>
                    <p class="company-ticker">${symbol}</p>
                </div>
            </div>

            <div class="company-details">
                <div class="detail-item">
                    <div class="detail-label">Market Cap</div>
                    <div class="detail-value large">${formatMarketCap(data.marketCapitalization)}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Industry</div>
                    <div class="detail-value">${data.finnhubIndustry || 'N/A'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Country</div>
                    <div class="detail-value">${data.country || 'N/A'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Currency</div>
                    <div class="detail-value">${data.currency || 'N/A'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Exchange</div>
                    <div class="detail-value">${data.exchange || 'N/A'}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">IPO Date</div>
                    <div class="detail-value">${data.ipo || 'N/A'}</div>
                </div>
            </div>

            ${data.weburl ? `
            <div class="company-metrics">
                <div class="metric-item">
                    <div class="metric-label">Website</div>
                    <div class="metric-value">
                        <a href="${data.weburl}" target="_blank" style="color: #60a5fa; text-decoration: none;">
                            ${data.weburl.replace(/^https?:\/\//, '').replace(/\/$/, '')}
                        </a>
                    </div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Employees</div>
                    <div class="metric-value">${formatEmployees(data.employeeTotal)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Shares Outstanding</div>
                    <div class="metric-value">${data.shareOutstanding ? `${(data.shareOutstanding / 1e6).toFixed(1)}M` : 'N/A'}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Phone</div>
                    <div class="metric-value">${data.phone || 'N/A'}</div>
                </div>
            </div>
            ` : ''}

            ${data.description ? `
            <div class="company-description">
                <h4>📋 About ${data.name}</h4>
                <p>${data.description}</p>
            </div>
            ` : ''}
        `;
    }

    renderErrorMessage(overlay, message) {
        const content = overlay.querySelector('.company-profile-content');
        content.innerHTML = `
            <button class="close-button" onclick="this.closest('.company-profile-overlay').remove()">×</button>
            <div class="error-message">
                <h3>❌ Error</h3>
                <p>${message}</p>
            </div>
        `;
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
        
        // Hide stock prices but keep headers clickable
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
            
            // Keep company name headers clickable
            const header = card.querySelector('h3');
            if (header) {
                header.style.pointerEvents = 'auto';
                header.style.cursor = 'pointer';
                header.style.opacity = '1';
            }
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