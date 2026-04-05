import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Date, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import relationship
from ..database import Base

def gen_uuid():
    return str(uuid.uuid4())

# ════════════════════════════════════════
# USER / AUTH
# ════════════════════════════════════════
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, default="")
    role = Column(String, default="engineer")  # admin, manager, engineer, accountant
    company_name = Column(String, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# ════════════════════════════════════════
# PROJECT
# ════════════════════════════════════════
class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    location = Column(String, default="")
    description = Column(Text, default="")
    status = Column(String, default="active")  # active, completed, on-hold
    budget = Column(Float, default=0)
    spent = Column(Float, default=0)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    owner_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    phases = relationship("ProjectPhase", back_populates="project", cascade="all, delete-orphan")
    materials = relationship("Material", back_populates="project", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="project", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="project", cascade="all, delete-orphan")
    workers = relationship("Worker", back_populates="project", cascade="all, delete-orphan")
    deliveries = relationship("Delivery", back_populates="project", cascade="all, delete-orphan")

class ProjectPhase(Base):
    __tablename__ = "project_phases"
    id = Column(String, primary_key=True, default=gen_uuid)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    budget = Column(Float, default=0)
    spent = Column(Float, default=0)
    status = Column(String, default="pending")  # pending, in-progress, completed
    project = relationship("Project", back_populates="phases")

# ════════════════════════════════════════
# MATERIAL / INVENTORY
# ════════════════════════════════════════
class Material(Base):
    __tablename__ = "materials"
    id = Column(String, primary_key=True, default=gen_uuid)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    category = Column(String, default="")
    unit = Column(String, default="Units")
    current_stock = Column(Float, default=0)
    min_stock = Column(Float, default=0)
    max_stock = Column(Float, default=0)
    unit_price = Column(Float, default=0)
    supplier = Column(String, default="")
    daily_usage_rate = Column(Float, default=0)
    qr_code = Column(String, default="")
    last_restocked = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="materials")
    logs = relationship("MaterialLog", back_populates="material", cascade="all, delete-orphan")

class MaterialLog(Base):
    __tablename__ = "material_logs"
    id = Column(String, primary_key=True, default=gen_uuid)
    material_id = Column(String, ForeignKey("materials.id", ondelete="CASCADE"))
    log_type = Column(String, nullable=False)  # in, out
    quantity = Column(Float, nullable=False)
    date = Column(Date, default=date.today)
    note = Column(Text, default="")
    logged_by = Column(String, default="")
    geo_lat = Column(Float, nullable=True)
    geo_lng = Column(Float, nullable=True)
    geo_address = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    material = relationship("Material", back_populates="logs")

# ════════════════════════════════════════
# TRANSACTION / PAYMENT
# ════════════════════════════════════════
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, default=gen_uuid)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"))
    tx_type = Column(String, nullable=False)  # payment, receipt
    category = Column(String, default="labor")  # labor, material, equipment, overhead, supplier
    amount = Column(Float, nullable=False)
    date = Column(Date, default=date.today)
    description = Column(Text, default="")
    status = Column(String, default="completed")  # completed, pending, failed
    payee = Column(String, default="")
    method = Column(String, default="bank")  # cash, bank, upi, cheque
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="transactions")

# ════════════════════════════════════════
# INVOICE
# ════════════════════════════════════════
class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(String, primary_key=True, default=gen_uuid)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"))
    invoice_number = Column(String, unique=True, nullable=False)
    inv_type = Column(String, default="supplier")  # supplier, client, internal
    amount = Column(Float, default=0)
    tax = Column(Float, default=0)
    total = Column(Float, default=0)
    date = Column(Date, default=date.today)
    due_date = Column(Date, nullable=True)
    status = Column(String, default="pending")  # paid, pending, overdue, draft
    party_name = Column(String, default="")
    party_contact = Column(String, default="")
    reconciled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(String, primary_key=True, default=gen_uuid)
    invoice_id = Column(String, ForeignKey("invoices.id", ondelete="CASCADE"))
    description = Column(String, default="")
    quantity = Column(Float, default=0)
    unit = Column(String, default="Units")
    unit_price = Column(Float, default=0)
    total = Column(Float, default=0)
    invoice = relationship("Invoice", back_populates="items")

# ════════════════════════════════════════
# WORKER
# ════════════════════════════════════════
class Worker(Base):
    __tablename__ = "workers"
    id = Column(String, primary_key=True, default=gen_uuid)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    role = Column(String, default="")
    pay_type = Column(String, default="weekly")  # daily, weekly, monthly
    rate = Column(Float, default=0)
    phone = Column(String, default="")
    join_date = Column(Date, nullable=True)
    status = Column(String, default="active")  # active, inactive
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="workers")

# ════════════════════════════════════════
# DELIVERY (GEO-TAGGED)
# ════════════════════════════════════════
class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(String, primary_key=True, default=gen_uuid)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"))
    material_id = Column(String, ForeignKey("materials.id", ondelete="SET NULL"), nullable=True)
    material_name = Column(String, default="")
    supplier = Column(String, default="")
    quantity = Column(Float, default=0)
    unit = Column(String, default="Units")
    expected_date = Column(Date, nullable=True)
    status = Column(String, default="expected")  # expected, in-transit, delivered, cancelled
    geo_lat = Column(Float, nullable=True)
    geo_lng = Column(Float, nullable=True)
    geo_address = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="deliveries")

# ════════════════════════════════════════
# ALERT
# ════════════════════════════════════════
class Alert(Base):
    __tablename__ = "alerts"
    id = Column(String, primary_key=True, default=gen_uuid)
    project_id = Column(String, nullable=True)
    alert_type = Column(String, default="info")  # low-stock, budget-overrun, payment-due, delivery, ai-insight, reconciliation
    title = Column(String, default="")
    message = Column(Text, default="")
    severity = Column(String, default="info")  # info, warning, critical
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
