/**
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
