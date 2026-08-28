/**
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
