"""Data models."""
# pylint: disable=no-member
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class HWProducts(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'hw_products'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    sw_id = db.Column(
        db.Integer, 
        db.ForeignKey('sw_products.id'), 
        nullable=False
        )
    hw_company_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    hw_company_product = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    #
    hw_hardware_components = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )
    #
    hw_categories = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    hw_product_description = db.Column(
        db.String, 
        unique=False, 
        nullable=False
    )
    hw_product_img = db.Column(
        db.String, 
        unique=False,
        nullable=False
    )
    hw_references = db.Column(
        db.String(80),
        unique=False,
        nullable=False
    )
    #
    # sw_company_product_id= db.Column(
    #     db.Integer,
    #     index=True,
    #     unique=False,
    #     nullable=False
    # )
    
    hw_locations_desc = db.Column(
        db.String, 
        default=None, 
        nullable=False
    )
    hw_locations_img = db.Column(
        db.String, 
        default=None, 
        nullable=False
    )
    # crops_id = db.Column(
    #     db.Integer,
    #     index=True,
    #     unique=False,
    #     nullable=False
    # )
    # spells_id = db.Column(
    #     db.Integer,
    #     default=None, 
    #     nullable=False
    # )
  
    def __init__(self, sw_id, hw_company_name, hw_company_product, hw_hardware_components, hw_categories, hw_product_description, hw_product_img, hw_references, hw_locations_desc, hw_locations_img ):
        self.sw_id=sw_id
        self.hw_company_name = hw_company_name
        self.hw_company_product = hw_company_product
        self.hw_hardware_components = hw_hardware_components
        self.hw_categories = hw_categories
        self.hw_product_description = hw_product_description
        self.hw_product_img = hw_product_img
        # self.sw_company_product = sw_company_product
        self.hw_locations_desc = hw_locations_desc
        self.hw_locations_img = hw_locations_img
        self.hw_references = hw_references
        # self.crops_id = crops_id
        # self.spells_id = spells_id
        print(repr(self.hw_company_name))
        print(repr(self.hw_company_product))
        print(repr(self.hw_product_img))
        tellme=type(self.hw_company_name)
        print(tellme)


class SWProducts(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'sw_products'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    sw_company_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    sw_company_product = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    #
    sw_software_components = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )
    #
    sw_categories = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    sw_product_description = db.Column(
        db.String, 
        unique=False, 
        nullable=False
    )
    sw_product_img = db.Column(
        db.String, 
        unique=False,
        nullable=False
    )
    sw_os_license = db.Column(
        db.String, 
        unique=False,
        nullable=False
    )
    sw_references = db.Column(
        db.String(80),
        unique=False,
        nullable=False
    )
    sw_locations_desc = db.Column(
        db.String, 
        default=None, 
        nullable=False
    )
    sw_locations_img = db.Column(
        db.String, 
        default=None, 
        nullable=False
    )
    # crops_id = db.Column(
    #     db.Integer,
    #     index=True,
    #     unique=False,
    #     nullable=False
    # )
    # spells_id = db.Column(
    #     db.Integer,
    #     default=None, 
    #     nullable=False
    # )
  
    def __init__(self, sw_company_name, sw_company_product, sw_software_components, sw_categories, sw_product_description, sw_product_img, sw_os_license, sw_references, sw_locations_desc, sw_locations_img ):
        self.sw_company_name = sw_company_name
        self.sw_company_product = sw_company_product
        self.sw_software_components = sw_software_components
        self.sw_categories = sw_categories
        self.sw_product_description = sw_product_description
        self.sw_product_img = sw_product_img
        self.sw_os_license = sw_os_license
        self.sw_locations_desc = sw_locations_desc
        self.sw_locations_img = sw_locations_img
        self.sw_references = sw_references
        print(repr(self.sw_company_name))
        print(repr(self.sw_company_product))
        print(repr(self.sw_product_img))
        tellme=type(self.sw_company_name)
        print(tellme)
        
