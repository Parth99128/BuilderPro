"""Automated invoice reconciliation engine.
Matches invoices against payment transactions by amount and party name.
"""
from typing import List, Dict
from ..models.models import Invoice, Transaction


def reconcile_invoices(invoices: List[Invoice], transactions: List[Transaction]) -> Dict:
    """
    Match invoices to payments. An invoice is considered reconciled if:
    1. It's already marked 'paid', OR
    2. A completed payment exists with matching amount (±1%) and
       party name overlap.
    """
    matched_ids = []
    unmatched_ids = []

    completed_payments = [
        tx for tx in transactions
        if tx.tx_type == "payment" and tx.status == "completed"
    ]

    used_tx_ids = set()

    for inv in invoices:
        if inv.status == "paid":
            matched_ids.append(inv.id)
            continue

        found = False
        for tx in completed_payments:
            if tx.id in used_tx_ids:
                continue

            # Amount match within 1%
            if inv.total > 0 and abs(tx.amount - inv.total) / inv.total <= 0.01:
                # Name overlap check
                inv_words = set(inv.party_name.lower().split())
                tx_words = set(tx.payee.lower().split())
                if inv_words & tx_words:  # at least one word in common
                    matched_ids.append(inv.id)
                    used_tx_ids.add(tx.id)
                    found = True
                    break

        if not found:
            unmatched_ids.append(inv.id)

    return {
        "total_invoices": len(invoices),
        "matched": len(matched_ids),
        "unmatched": len(unmatched_ids),
        "matched_ids": matched_ids,
        "unmatched_ids": unmatched_ids,
    }
