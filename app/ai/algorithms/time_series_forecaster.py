import math
from typing import List, Dict, Any, Tuple, Optional


class AdvancedTimeSeriesForecaster:
    """Mathematical time-series forecasting engine with Holt-Winters Exponential Smoothing,
    trend decomposition, seasonality adjustments, and dynamic confidence intervals."""

    @staticmethod
    def moving_average(series: List[float], window: int = 7) -> List[float]:
        """Compute simple moving average over sliding window."""
        if not series or window <= 0:
            return []
        result = []
        for i in range(len(series)):
            start_idx = max(0, i - window + 1)
            window_slice = series[start_idx : i + 1]
            result.append(sum(window_slice) / len(window_slice))
        return result

    @staticmethod
    def exponential_smoothing(series: List[float], alpha: float = 0.3) -> List[float]:
        """Compute single exponential smoothing."""
        if not series:
            return []
        smoothed = [series[0]]
        for t in range(1, len(series)):
            val = alpha * series[t] + (1 - alpha) * smoothed[t - 1]
            smoothed.append(val)
        return smoothed

    @staticmethod
    def holt_linear_trend(
        series: List[float],
        horizon: int = 14,
        alpha: float = 0.3,
        beta: float = 0.1
    ) -> Dict[str, Any]:
        """Holt's Double Exponential Smoothing (level + trend) with multi-step future projection."""
        if len(series) < 2:
            base_val = series[0] if series else 1.0
            return {
                'level': base_val,
                'trend': 0.0,
                'forecast': [max(0.0, base_val)] * horizon,
                'fitted': [base_val] * len(series)
            }

        # Initialization
        level = series[0]
        trend = series[1] - series[0]
        fitted = [level]

        for t in range(1, len(series)):
            last_level = level
            level = alpha * series[t] + (1 - alpha) * (level + trend)
            trend = beta * (level - last_level) + (1 - beta) * trend
            fitted.append(level + trend)

        # Generate future projection
        forecast = []
        for h in range(1, horizon + 1):
            pred = max(0.0, level + h * trend)
            forecast.append(round(pred, 2))

        return {
            'level': round(level, 4),
            'trend': round(trend, 4),
            'forecast': forecast,
            'fitted': [round(f, 2) for f in fitted]
        }

    @classmethod
    def holt_winters_forecast(
        cls,
        series: List[float],
        season_length: int = 7,
        horizon: int = 14,
        alpha: float = 0.25,
        beta: float = 0.08,
        gamma: float = 0.15
    ) -> Dict[str, Any]:
        """Triple Exponential Smoothing with additive seasonality and statistical confidence bounds."""
        n = len(series)
        if n < season_length * 2:
            # Fallback to Holt's Linear Trend if historical data is shorter than two complete seasons
            return cls.holt_linear_trend(series, horizon=horizon, alpha=alpha, beta=beta)

        # Initial season indices
        season_averages = []
        for i in range(2):
            season_slice = series[i * season_length : (i + 1) * season_length]
            season_averages.append(sum(season_slice) / season_length)

        # Initial trend and level
        trend = (season_averages[1] - season_averages[0]) / season_length
        level = season_averages[0]

        # Initial seasonal factors
        seasonal = [0.0] * season_length
        for i in range(season_length):
            seasonal[i] = series[i] - season_averages[0]

        fitted = []
        residuals = []

        # Iterate through historical observations
        for i in range(n):
            val = series[i]
            season_idx = i % season_length
            prev_level = level
            
            # Update equations (additive)
            level = alpha * (val - seasonal[season_idx]) + (1 - alpha) * (prev_level + trend)
            trend = beta * (level - prev_level) + (1 - beta) * trend
            seasonal[season_idx] = gamma * (val - level) + (1 - gamma) * seasonal[season_idx]

            pred = max(0.0, prev_level + trend + seasonal[season_idx])
            fitted.append(pred)
            residuals.append(val - pred)

        # Calculate residual standard deviation for confidence interval bands
        variance = sum(r ** 2 for r in residuals) / max(1, n - 1)
        sigma = math.sqrt(variance)

        # Generate forward horizon projections with 95% confidence intervals (Z = 1.96)
        projections = []
        for h in range(1, horizon + 1):
            season_idx = (n + h - 1) % season_length
            point_pred = max(0.0, level + h * trend + seasonal[season_idx])
            margin = 1.96 * sigma * math.sqrt(h)
            lower_bound = max(0.0, point_pred - margin)
            upper_bound = point_pred + margin

            projections.append({
                'horizon_step': h,
                'forecast': round(point_pred, 2),
                'lower_95': round(lower_bound, 2),
                'upper_95': round(upper_bound, 2)
            })

        return {
            'method': 'holt_winters_additive',
            'level': round(level, 4),
            'trend': round(trend, 4),
            'residual_std': round(sigma, 4),
            'forecast_points': projections,
            'fitted_series': [round(x, 2) for x in fitted]
        }
