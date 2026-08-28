# ShopSense AI ES6+ Modular JavaScript Generator
from pathlib import Path

BASE_JS = Path(__file__).resolve().parent.parent / 'app' / 'static' / 'js'
(BASE_JS / 'core').mkdir(parents=True, exist_ok=True)
(BASE_JS / 'cart').mkdir(parents=True, exist_ok=True)
(BASE_JS / 'wishlist').mkdir(parents=True, exist_ok=True)
(BASE_JS / 'copilot').mkdir(parents=True, exist_ok=True)
(BASE_JS / 'missions').mkdir(parents=True, exist_ok=True)
(BASE_JS / 'seller').mkdir(parents=True, exist_ok=True)

# 1. core/api_client.js
(BASE_JS / 'core' / 'api_client.js').write_text('''/**
 * ShopSense AI — Robust Client API Wrapper
 */
const ShopSenseAPI = {
    async request(url, options = {}) {
        const defaultHeaders = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };

        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...(options.headers || {})
            }
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                const errorMsg = data.error || data.message || `Request failed with status ${response.status}`;
                throw new Error(errorMsg);
            }
            return data;
        } catch (err) {
            console.error(`API Error [${url}]:`, err);
            throw err;
        }
    },

    get(url, params = {}) {
        const query = new URLSearchParams(params).toString();
        const fullUrl = query ? `${url}?${query}` : url;
        return this.request(fullUrl, { method: 'GET' });
    },

    post(url, body = {}) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(body)
        });
    },

    delete(url) {
        return this.request(url, { method: 'DELETE' });
    }
};

window.ShopSenseAPI = ShopSenseAPI;
''', encoding='utf-8')

# 2. core/toast.js
(BASE_JS / 'core' / 'toast.js').write_text('''/**
 * ShopSense AI — Toast Notification System
 */
const ShopSenseToast = {
    show(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let iconName = 'info';
        if (type === 'success') iconName = 'check-circle';
        if (type === 'danger' || type === 'error') iconName = 'alert-circle';
        if (type === 'warning') iconName = 'alert-triangle';

        toast.innerHTML = `
            <i data-lucide="${iconName}"></i>
            <span>${message}</span>
        `;
        container.appendChild(toast);
        
        if (window.lucide) window.lucide.createIcons();

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(12px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    },

    success(msg) { this.show(msg, 'success'); },
    error(msg) { this.show(msg, 'danger'); },
    info(msg) { this.show(msg, 'info'); },
    warning(msg) { this.show(msg, 'warning'); }
};

window.ShopSenseToast = ShopSenseToast;
''', encoding='utf-8')

# 3. core/state.js
(BASE_JS / 'core' / 'state.js').write_text('''/**
 * ShopSense AI — Global Client State Manager
 */
const ShopSenseState = {
    cartCount: 0,
    wishlistItems: new Set(),

    updateCartBadge(count) {
        this.cartCount = count;
        const el = document.getElementById('nav-cart-count');
        if (el) {
            el.textContent = count;
            el.style.display = count > 0 ? 'inline-block' : 'none';
        }
    },

    updateWishlistBadge(count) {
        const el = document.getElementById('nav-wishlist-count');
        if (el) {
            el.textContent = count;
            el.style.display = count > 0 ? 'inline-block' : 'none';
        }
    }
};

window.ShopSenseState = ShopSenseState;
''', encoding='utf-8')

# 4. cart/cart.js
(BASE_JS / 'cart' / 'cart.js').write_text('''/**
 * ShopSense AI — Cart Interactions
 */
const ShopSenseCart = {
    async add(productId, quantity = 1) {
        try {
            const res = await ShopSenseAPI.post('/api/cart/add', {
                product_id: productId,
                quantity: quantity
            });
            if (res.success) {
                ShopSenseState.updateCartBadge(res.cart.total_items_count);
                ShopSenseToast.success('Item added to cart!');
            }
        } catch (err) {
            ShopSenseToast.error(err.message || 'Failed to add item to cart');
        }
    },

    async update(cartItemId, quantity) {
        try {
            const res = await ShopSenseAPI.post('/api/cart/update', {
                cart_item_id: cartItemId,
                quantity: parseInt(quantity, 10)
            });
            if (res.success) {
                ShopSenseState.updateCartBadge(res.cart.total_items_count);
                location.reload();
            }
        } catch (err) {
            ShopSenseToast.error(err.message || 'Failed to update quantity');
        }
    },

    async remove(cartItemId) {
        try {
            const res = await ShopSenseAPI.post(`/api/cart/remove/${cartItemId}`);
            if (res.success) {
                ShopSenseState.updateCartBadge(res.cart.total_items_count);
                const row = document.getElementById(`cart-item-${cartItemId}`);
                if (row) row.remove();
                ShopSenseToast.info('Item removed from cart');
                setTimeout(() => location.reload(), 500);
            }
        } catch (err) {
            ShopSenseToast.error(err.message || 'Failed to remove item');
        }
    }
};

window.ShopSenseCart = ShopSenseCart;
''', encoding='utf-8')

# 5. wishlist/wishlist.js
(BASE_JS / 'wishlist' / 'wishlist.js').write_text('''/**
 * ShopSense AI — Wishlist Interactions
 */
const ShopSenseWishlist = {
    async toggle(productId, buttonElement) {
        try {
            const res = await ShopSenseAPI.post('/api/wishlist/toggle', { product_id: productId });
            if (buttonElement) {
                buttonElement.classList.toggle('active', res.is_wishlisted);
            }
            ShopSenseState.updateWishlistBadge(res.wishlist.total_items_count);
            if (res.is_wishlisted) {
                ShopSenseToast.success('Saved to wishlist');
            } else {
                ShopSenseToast.info('Removed from wishlist');
                const itemEl = document.getElementById(`wishlist-item-${productId}`);
                if (itemEl) itemEl.remove();
            }
        } catch (err) {
            ShopSenseToast.error(err.message || 'Please log in to manage your wishlist');
        }
    }
};

window.ShopSenseWishlist = ShopSenseWishlist;
''', encoding='utf-8')

# 6. copilot/copilot.js
(BASE_JS / 'copilot' / 'copilot.js').write_text('''/**
 * ShopSense AI — Shopping Copilot Chat Stream Handler
 */
const ShopSenseCopilot = {
    activeConversationId: null,

    async sendMessage(event) {
        event.preventDefault();
        const input = document.getElementById('copilot-input');
        const stream = document.getElementById('chat-stream');
        const text = input.value.trim();
        if (!text) return;

        // Render user message bubble
        this.appendMessage('user', text);
        input.value = '';

        // Render loading state
        const loadingId = 'loading-' + Date.now();
        this.appendLoading(loadingId);

        try {
            const res = await ShopSenseAPI.post('/api/copilot/chat', {
                conversation_id: this.activeConversationId,
                message: text
            });

            document.getElementById(loadingId)?.remove();

            if (res.conversation_id) {
                this.activeConversationId = res.conversation_id;
            }

            // Render bot explanation bubble with product cards
            this.renderAssistantResponse(res);
        } catch (err) {
            document.getElementById(loadingId)?.remove();
            this.appendMessage('bot', `Sorry, I encountered an issue: ${err.message}`);
        }
    },

    appendMessage(sender, text) {
        const stream = document.getElementById('chat-stream');
        if (!stream) return;

        const bubble = document.createElement('div');
        bubble.className = `chat-bubble ${sender}`;
        
        if (sender === 'bot') {
            bubble.innerHTML = `
                <div class="bot-avatar"><i data-lucide="bot"></i></div>
                <div class="bubble-content"><p>${text}</p></div>
            `;
        } else {
            bubble.innerHTML = `
                <div class="bubble-content"><p>${text}</p></div>
            `;
        }

        stream.appendChild(bubble);
        stream.scrollTop = stream.scrollHeight;
        if (window.lucide) window.lucide.createIcons();
    },

    appendLoading(id) {
        const stream = document.getElementById('chat-stream');
        const bubble = document.createElement('div');
        bubble.id = id;
        bubble.className = 'chat-bubble bot loading';
        bubble.innerHTML = `
            <div class="bot-avatar"><i data-lucide="bot"></i></div>
            <div class="bubble-content"><p><em>Analyzing requirements & ranking catalog...</em></p></div>
        `;
        stream.appendChild(bubble);
        stream.scrollTop = stream.scrollHeight;
        if (window.lucide) window.lucide.createIcons();
    },

    renderAssistantResponse(res) {
        const stream = document.getElementById('chat-stream');
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble bot';

        let productsHtml = '';
        if (res.recommended_products && res.recommended_products.length > 0) {
            productsHtml = '<div class="copilot-rec-stream">';
            res.recommended_products.forEach(item => {
                const p = item.product;
                const badge = item.badge ? `<span class="badge badge-accent">${item.badge}</span>` : '';
                productsHtml += `
                    <div class="copilot-product-card">
                        ${badge}
                        <div class="copilot-score">Match Score: <strong>${item.match_score}%</strong></div>
                        <h4><a href="/products/${p.slug}" target="_blank">${p.title}</a></h4>
                        <div class="copilot-card-price">₹${p.current_price.toLocaleString()}</div>
                        <ul class="copilot-reasons">
                            ${(item.reasons || []).map(r => `<li>&bull; ${r}</li>`).join('')}
                        </ul>
                        <button class="btn btn-primary btn-sm" onclick="ShopSenseCart.add(${p.id}, 1)">Add to Cart</button>
                    </div>
                `;
            });
            productsHtml += '</div>';
        }

        bubble.innerHTML = `
            <div class="bot-avatar"><i data-lucide="bot"></i></div>
            <div class="bubble-content">
                <p>${res.message.content}</p>
                ${res.explanation ? `<div class="copilot-explanation-box"><strong>Why this fits:</strong> ${res.explanation}</div>` : ''}
                ${productsHtml}
            </div>
        `;

        stream.appendChild(bubble);
        stream.scrollTop = stream.scrollHeight;
        if (window.lucide) window.lucide.createIcons();
    },

    newSession() {
        this.activeConversationId = null;
        const stream = document.getElementById('chat-stream');
        if (stream) {
            stream.innerHTML = `
                <div class="chat-bubble bot">
                    <div class="bot-avatar"><i data-lucide="bot"></i></div>
                    <div class="bubble-content">
                        <p>New session initialized. How can I assist your product selection today?</p>
                    </div>
                </div>
            `;
            if (window.lucide) window.lucide.createIcons();
        }
    },

    async loadSession(convId) {
        this.activeConversationId = convId;
        try {
            const res = await ShopSenseAPI.get(`/api/copilot/conversations/${convId}`);
            const stream = document.getElementById('chat-stream');
            if (stream && res.conversation.messages) {
                stream.innerHTML = '';
                res.conversation.messages.forEach(msg => {
                    this.appendMessage(msg.sender === 'assistant' ? 'bot' : 'user', msg.content);
                });
            }
        } catch (err) {
            ShopSenseToast.error('Failed to load session history');
        }
    }
};

window.ShopSenseCopilot = ShopSenseCopilot;
''', encoding='utf-8')

# 7. missions/missions.js
(BASE_JS / 'missions' / 'missions.js').write_text('''/**
 * ShopSense AI — Shopping Missions Basket Optimizer
 */
const ShopSenseMissions = {
    async build(event) {
        event.preventDefault();
        const prompt = document.getElementById('mission-prompt').value.trim();
        const budget = parseFloat(document.getElementById('mission-budget').value);
        const mode = document.getElementById('mission-mode').value;
        const resultArea = document.getElementById('mission-result-area');
        const btn = document.getElementById('btn-build-mission');

        btn.disabled = true;
        btn.innerHTML = 'Optimizing basket...';

        try {
            const res = await ShopSenseAPI.post('/api/missions/build', {
                prompt: prompt,
                target_budget: budget,
                optimization_mode: mode
            });

            if (res.success) {
                this.renderMissionBasket(res.mission, resultArea);
                ShopSenseToast.success('Optimized basket created!');
            }
        } catch (err) {
            ShopSenseToast.error(err.message || 'Failed to solve mission');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i data-lucide="sparkles"></i> Generate Optimized Basket';
            if (window.lucide) window.lucide.createIcons();
        }
    },

    renderMissionBasket(mission, container) {
        let itemsHtml = '';
        mission.items.forEach(item => {
            itemsHtml += `
                <div class="mission-slot-card">
                    <div class="slot-role-badge">${item.slot_role}</div>
                    <h4><a href="/products/${item.product.slug}" target="_blank">${item.product.title}</a></h4>
                    <div class="slot-price-row">
                        <span class="slot-price">₹${item.actual_price.toLocaleString()}</span>
                        <small class="text-muted">(Budget Allocated: ₹${item.assigned_budget.toLocaleString()})</small>
                    </div>
                    <p class="slot-rationale">${item.selection_rationale}</p>
                    <button class="btn btn-primary btn-sm" onclick="ShopSenseCart.add(${item.product.id}, 1)">Add to Cart</button>
                </div>
            `;
        });

        container.innerHTML = `
            <div class="mission-result-card">
                <div class="mission-result-header">
                    <h2>${mission.title}</h2>
                    <div class="mission-budget-summary">
                        <span>Total Target: <strong>₹${mission.target_budget.toLocaleString()}</strong></span>
                        <span>Estimated Cost: <strong>₹${mission.allocated_total.toLocaleString()}</strong></span>
                        <span class="badge badge-success">Saved: ₹${mission.savings_amount.toLocaleString()}</span>
                    </div>
                </div>
                <p class="mission-rationale-text">${mission.ai_rationale}</p>
                <div class="mission-slots-grid">
                    ${itemsHtml}
                </div>
            </div>
        `;
        if (window.lucide) window.lucide.createIcons();
    }
};

window.ShopSenseMissions = ShopSenseMissions;
''', encoding='utf-8')

# 8. seller/seller.js
(BASE_JS / 'seller' / 'seller.js').write_text('''/**
 * ShopSense AI — Seller Portal Analytics & Inventory Management
 */
const ShopSenseSeller = {
    async restock(inventoryId, productTitle) {
        const qty = prompt(`Enter restock quantity for "${productTitle}":`, "50");
        if (!qty || isNaN(qty) || parseInt(qty, 10) <= 0) return;

        try {
            const res = await ShopSenseAPI.post('/api/seller/inventory/restock', {
                inventory_id: inventoryId,
                quantity: parseInt(qty, 10)
            });
            if (res.success) {
                ShopSenseToast.success(`Restocked ${qty} units successfully.`);
                setTimeout(() => location.reload(), 600);
            }
        } catch (err) {
            ShopSenseToast.error(err.message || 'Restock failed');
        }
    },

    async fetchForecast(productId) {
        const area = document.getElementById('forecast-output-area');
        if (!area || !productId) return;

        area.innerHTML = '<div class="empty-state"><p>Calculating time-series model projections...</p></div>';

        try {
            const res = await ShopSenseAPI.get(`/api/seller/forecast/${productId}`);
            let rowsHtml = '';
            res.daily_projections.forEach(p => {
                rowsHtml += `
                    <tr>
                        <td>Day ${p.day} (${p.date})</td>
                        <td><strong>${p.predicted_units} units</strong></td>
                        <td>${p.cumulative_units} units</td>
                    </tr>
                `;
            });

            area.innerHTML = `
                <div class="forecast-card-result">
                    <div class="forecast-metrics-grid">
                        <div class="f-metric">Current Stock: <strong>${res.current_stock}</strong></div>
                        <div class="f-metric">14-Day Demand: <strong>${res.predicted_demand_total} units</strong></div>
                        <div class="f-metric ${res.stockout_predicted ? 'danger' : 'success'}">
                            Stockout Predicted: <strong>${res.stockout_predicted ? `YES (~${res.estimated_days_to_stockout} days)` : 'NO'}</strong>
                        </div>
                        <div class="f-metric">Reorder Recommendation: <strong>${res.recommended_reorder_qty} units</strong></div>
                    </div>
                    <table class="table table-compact" style="margin-top: 1.5rem;">
                        <thead>
                            <tr><th>Date / Projection Horizon</th><th>Daily Forecasted Demand</th><th>Cumulative Units</th></tr>
                        </thead>
                        <tbody>${rowsHtml}</tbody>
                    </table>
                </div>
            `;
        } catch (err) {
            area.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
        }
    }
};

window.ShopSenseSeller = ShopSenseSeller;
''', encoding='utf-8')

# 9. seller/seller_copilot.js
(BASE_JS / 'seller' / 'seller_copilot.js').write_text('''/**
 * ShopSense AI — Seller Diagnostic Copilot
 */
const ShopSenseSellerCopilot = {
    ask(question) {
        const input = document.getElementById('seller-copilot-input');
        if (input) {
            input.value = question;
            this.send({ preventDefault: () => {} });
        }
    },

    async send(event) {
        event.preventDefault();
        const input = document.getElementById('seller-copilot-input');
        const stream = document.getElementById('seller-chat-stream');
        const query = input.value.trim();
        if (!query) return;

        // Render user message
        const userBubble = document.createElement('div');
        userBubble.className = 'chat-bubble user';
        userBubble.innerHTML = `<div class="bubble-content"><p>${query}</p></div>`;
        stream.appendChild(userBubble);
        input.value = '';

        // Loading
        const loadingBubble = document.createElement('div');
        loadingBubble.className = 'chat-bubble bot loading';
        loadingBubble.innerHTML = `<div class="bot-avatar"><i data-lucide="bot"></i></div><div class="bubble-content"><p><em>Querying sales telemetry, stock levels, and review sentiments...</em></p></div>`;
        stream.appendChild(loadingBubble);
        stream.scrollTop = stream.scrollHeight;
        if (window.lucide) window.lucide.createIcons();

        try {
            const res = await ShopSenseAPI.post('/api/seller/copilot/chat', { query: query });
            loadingBubble.remove();

            const botBubble = document.createElement('div');
            botBubble.className = 'chat-bubble bot';

            let diagHtml = '';
            if (res.diagnostic) {
                diagHtml = `
                    <div class="diagnostic-box">
                        <h4>Diagnostic Telemetry (${res.diagnostic.product_title}):</h4>
                        <ul>
                            ${res.diagnostic.findings.map(f => `<li><strong>Finding:</strong> ${f}</li>`).join('')}
                        </ul>
                        <div class="diag-recs">
                            <strong>Recommended Business Actions:</strong>
                            <ul>${res.diagnostic.recommendations.map(r => `<li>&bull; ${r}</li>`).join('')}</ul>
                        </div>
                    </div>
                `;
            }

            botBubble.innerHTML = `
                <div class="bot-avatar"><i data-lucide="bot"></i></div>
                <div class="bubble-content">
                    <p>${res.response}</p>
                    ${diagHtml}
                </div>
            `;
            stream.appendChild(botBubble);
            stream.scrollTop = stream.scrollHeight;
            if (window.lucide) window.lucide.createIcons();
        } catch (err) {
            loadingBubble.remove();
            ShopSenseToast.error(err.message || 'Diagnostic failed');
        }
    }
};

window.ShopSenseSellerCopilot = ShopSenseSellerCopilot;
''', encoding='utf-8')

print('All 9 ES6+ JavaScript modules generated successfully!')
