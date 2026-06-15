from sqlalchemy import Column, BigInteger, Text, Numeric, Date, DateTime, CheckConstraint, text, Boolean
from database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_file_id = Column(Text, nullable=False)
    original_filename = Column(Text, nullable=False)
    mime_type = Column(Text, default="application/pdf", nullable=False)
    google_drive_file_id = Column(Text, nullable=False)
    google_drive_link = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, server_default=text("now()"), nullable=False)
    summary_text = Column(Text, nullable=True)
    summary_status = Column(Text, default="pending", nullable=False)
    notes = Column(Text, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    disabled = Column(Boolean, default=False)


class FinanceMovement(Base):
    __tablename__ = "finance_movements"
    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_finance_movements_amount_positive"),
        CheckConstraint(
            "type = ANY (ARRAY['income'::text, 'expense'::text])",
            name="ck_finance_movements_type",
        ),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type = Column(Text, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    movement_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    origin = Column(Text, default="telegram_manual", nullable=False)
    created_at = Column(DateTime, server_default=text("now()"), nullable=False)
