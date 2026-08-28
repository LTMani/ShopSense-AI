/**
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
