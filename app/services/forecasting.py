"""AI-based demand forecasting using scikit-learn linear regression.
Works entirely offline — no external API needed.
If an AI API key is configured, it could be extended to call external services.
"""
import math
from datetime import date, timedelta
from typing import List, Dict
import numpy as np
from sklearn.linear_model import LinearRegression

from ..models.models import Material, MaterialLog


def forecast_material(material: Material, logs: List[MaterialLog]) -> Dict:
    """
    Predict days until depletion, recommended reorder quantity,
    usage trend, and confidence score using linear regression.
    """
    # Collect "out" logs sorted by date
    out_logs = sorted(
        [l for l in logs if l.log_type == "out"],
        key=lambda l: l.date if l.date else date.today()
    )

    daily_rate = material.daily_usage_rate if material.daily_usage_rate > 0 else 0
    trend = "stable"
    confidence = 0.5

    if len(out_logs) >= 5:
        # Build daily usage array for regression
        usage_by_day: Dict[date, float] = {}
        for log in out_logs:
            d = log.date if log.date else date.today()
            usage_by_day[d] = usage_by_day.get(d, 0) + log.quantity

        if len(usage_by_day) >= 3:
            sorted_days = sorted(usage_by_day.keys())
            base = sorted_days[0]
            X = np.array([(d - base).days for d in sorted_days]).reshape(-1, 1)
            y = np.array([usage_by_day[d] for d in sorted_days])

            model = LinearRegression()
            model.fit(X, y)

            # Predicted daily usage = model intercept + slope * current_day
            today_x = (date.today() - base).days
            predicted_daily = max(0, model.predict(np.array([[today_x]]))[0])

            if predicted_daily > 0:
                daily_rate = predicted_daily

            # Confidence from R²
            r2 = model.score(X, y)
            confidence = max(0.1, min(0.99, r2))

            # Trend from slope
            slope = model.coef_[0]
            if slope > 0.05 * np.mean(y):
                trend = "increasing"
            elif slope < -0.05 * np.mean(y):
                trend = "decreasing"
            else:
                trend = "stable"
    elif len(out_logs) > 0:
        # Simple average
        total_out = sum(l.quantity for l in out_logs)
        days_span = max(1, (date.today() - out_logs[0].date).days) if out_logs[0].date else 1
        daily_rate = total_out / days_span if days_span > 0 else daily_rate
        confidence = 0.3

    # Calculate predictions
    if daily_rate > 0:
        days_left = max(0, math.floor(material.current_stock / daily_rate))
        reorder_days = max(0, days_left - 5)  # order 5 days before depletion
        reorder_date = (date.today() + timedelta(days=reorder_days)).isoformat()
        recommended_qty = math.ceil(daily_rate * 30)  # 30 days supply
    else:
        days_left = 999
        reorder_date = ""
        recommended_qty = 0

    return {
        "material_id": material.id,
        "material_name": material.name,
        "current_stock": material.current_stock,
        "daily_usage_rate": round(daily_rate, 2),
        "days_left": days_left,
        "reorder_date": reorder_date,
        "recommended_qty": recommended_qty,
        "trend": trend,
        "confidence": round(confidence, 2),
    }


def forecast_all_materials(materials: List[Material], all_logs: List[MaterialLog]) -> List[Dict]:
    """Run forecast for every material."""
    results = []
    logs_by_mat = {}
    for log in all_logs:
        logs_by_mat.setdefault(log.material_id, []).append(log)
    for mat in materials:
        mat_logs = logs_by_mat.get(mat.id, [])
        results.append(forecast_material(mat, mat_logs))
    return results
