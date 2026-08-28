/**
 * ShopSense AI — Shopping Copilot Chat Stream Handler
 */
const ShopSenseCopilot = {
    activeConversationId: null,

    async sendMessage(event) {
        if (event && event.preventDefault) {
            event.preventDefault();
        }
        const input = document.getElementById('copilot-input');
        const stream = document.getElementById('chat-stream');
        const text = input ? input.value.trim() : '';
        if (!text) return;

        // Render user message bubble
        this.appendMessage('user', text);
        if (input) input.value = '';

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
    },

    sendPrompt(promptText) {
        const input = document.getElementById('copilot-input');
        if (input) {
            input.value = promptText;
            this.sendMessage();
        }
    }
};

window.ShopSenseCopilot = ShopSenseCopilot;
