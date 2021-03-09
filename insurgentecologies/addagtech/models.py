"""Data models."""
# pylint: disable=no-member
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CompanyProducts(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'company_products'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    company_name = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    company_product = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    img_url = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )
  
    def __repr__(self):
        return '<CompanyProducts {}>'.format(self.username)