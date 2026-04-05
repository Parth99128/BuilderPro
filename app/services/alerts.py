"""Smart alert generation engine.
Analyzes live data and produces actionable alerts.
"""
from datetime import date
from typing import List, Dict
from ..models.models import Project, Material, Invoice, Transaction, Delivery


def _fmt(n: float) -> str:
    if n >= 10_000_000:
        return f"\u20B9{n / 10_000_000:.2f} Cr"
    if n >= 100_000:
        return f"\u20B9{n / 100_000:.2f} L"
    if n >= 1000:
        return f"\u20B9{n / 1000:.1f}K"
    return f"\u20B9{n:,.0f}"


def generate_alerts(
    projects: List[Project],
    materials: List[Material],
    invoices: List[Invoice],
    transactions: List[Transaction],
    deliveries: List[Delivery],
) -> List[Dict]:
    alerts = []
    today = date.today()

    # ── Low stock ──
    for m in materials:
        if m.current_stock <= m.min_stock and m.min_stock > 0:
            sev = "critical" if m.current_stock <= m.min_stock * 0.5 else "warning"
            days_msg = ""
            if m.daily_usage_rate > 0:
                dl = int(m.current_stock / m.daily_usage_rate)
                days_msg = f" ~{dl} days remaining."
            alerts.append({
                "alert_type": "low-stock",
                "title": f"Low Stock: {m.name}",
                "message": f"{m.current_stock} {m.unit} left (min: {m.min_stock}).{days_msg}",
                "severity": sev,
                "project_id": m.project_id,
            })

        # Depletion warning
        if m.daily_usage_rate > 0 and m.current_stock > m.min_stock:
            dl = int(m.current_stock / m.daily_usage_rate)
            if 0 < dl <= 7:
                alerts.append({
                    "alert_type": "ai-insight",
                    "title": f"Depletion Warning: {m.name}",
                    "message": f"Will run out in ~{dl} days at {m.daily_usage_rate} {m.unit}/day. Reorder recommended.",
                    "severity": "info",
                    "project_id": m.project_id,
                })

    # ── Budget overrun ──
    for p in projects:
        if p.budget > 0 and p.status == "active":
            pct = p.spent / p.budget
            if pct >= 0.9:
                sev = "critical" if pct >= 1.0 else "warning"
                alerts.append({
                    "alert_type": "budget-overrun",
                    "title": f"Budget Alert: {p.name}",
                    "message": f"{pct * 100:.1f}% utilized ({_fmt(p.spent)} of {_fmt(p.budget)}). {_fmt(p.budget - p.spent)} remaining.",
                    "severity": sev,
                    "project_id": p.id,
                })

    # ── Overdue invoices ──
    for inv in invoices:
        if inv.status in ("pending", "overdue") and inv.due_date and inv.due_date < today:
            od = (today - inv.due_date).days
            sev = "critical" if od > 15 else "warning"
            alerts.append({
                "alert_type": "payment-due",
                "title": f"Overdue: {inv.invoice_number}",
                "message": f"{inv.party_name} - {_fmt(inv.total)} overdue by {od} day(s).",
                "severity": sev,
                "project_id": inv.project_id,
            })

    # ── Pending payments ──
    pending = [t for t in transactions if t.status == "pending"]
    if pending:
        total = sum(t.amount for t in pending)
        alerts.append({
            "alert_type": "payment-due",
            "title": f"{len(pending)} Pending Payment(s)",
            "message": f"Total: {_fmt(total)}. Process to avoid delays.",
            "severity": "critical" if len(pending) > 5 else "info",
            "project_id": None,
        })

    # ── Deliveries ──
    for d in deliveries:
        if d.status in ("expected", "in-transit"):
            geo = f" Location: {d.geo_address}" if d.geo_address else ""
            alerts.append({
                "alert_type": "delivery",
                "title": f"Delivery: {d.material_name}",
                "message": f"{d.quantity} {d.unit} from {d.supplier}. Expected: {d.expected_date}.{geo}",
                "severity": "info",
                "project_id": d.project_id,
            })

    return alerts
