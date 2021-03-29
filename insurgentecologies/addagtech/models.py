"""Data models."""
# pylint: disable=no-member
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

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
        nullable=True
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
    crops_id = db.Column(
        db.Integer, 
        db.ForeignKey('crops.id'), 
        nullable=True
    )
    # spells_id = db.Column(
    #     db.Integer,
    #     default=None, 
    #     nullable=False
    # )
  
    def __init__(self, sw_id, hw_company_name, hw_company_product, hw_hardware_components, hw_categories, hw_product_description, hw_product_img, hw_references, hw_locations_desc, hw_locations_img, crops_id):
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
        self.crops_id = crops_id
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
    crops_id = db.Column(
        db.Integer, 
        db.ForeignKey('crops.id'), 
        nullable=True
    )
    # spells_id = db.Column(
    #     db.Integer,
    #     default=None, 
    #     nullable=False
    # )
  
    def __init__(self, sw_company_name, sw_company_product, sw_software_components, sw_categories, sw_product_description, sw_product_img, sw_os_license, sw_references, sw_locations_desc, sw_locations_img, crops_id):
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
        self.crops_id = crops_id
        print(repr(self.sw_company_name))
        print(repr(self.sw_company_product))
        print(repr(self.sw_product_img))
        tellme=type(self.sw_company_name)
        print(tellme)
        

class Crops(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'crops'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    sw_id = db.Column(
        db.Integer, 
        db.ForeignKey('sw_products.id'), 
        nullable=True
    )
    hw_id = db.Column(
        db.Integer, 
        db.ForeignKey('hw_products.id'), 
        nullable=True
    )
    company_id = db.Column(
        db.Integer, 
        db.ForeignKey('companies.id'), 
        nullable=True
    )
    crop_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    genus_species = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    #
    crop_intellectual_property = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )
    #
    crop_chemicals_used = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    crop_genetic_information = db.Column(
        db.String, 
        unique=False, 
        nullable=False
    )
    crop_companions = db.Column(
        db.String, 
        unique=False,
        nullable=False
    )
    crop_description = db.Column(
        db.Text, 
        unique=False,
        nullable=False
    )
    crop_img = db.Column(
        db.String(80),
        unique=False,
        nullable=False
    )
    crop_references = db.Column(
        db.String, 
        default=None, 
        nullable=False
    )
    crop_locations = db.Column(
        db.Text, 
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
  
    def __init__(self, sw_id, hw_id, crop_name, company_id, genus_species, crop_intellectual_property, crop_chemicals_used, crop_genetic_information, crop_companions, crop_description, crop_img, crop_references, crop_locations ):
        self.sw_id = sw_id
        self.hw_id = hw_id
        self.company_id = company_id
        self.crop_name = crop_name
        self.genus_species = genus_species
        self.crop_intellectual_property = crop_intellectual_property
        self.crop_chemicals_used = crop_chemicals_used
        self.crop_genetic_information = crop_genetic_information
        self.crop_companions = crop_companions
        self.crop_description = crop_description
        self.crop_img = crop_img
        self.crop_references = crop_references
        self.crop_locations = crop_locations


class Companies(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'companies'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    hw_id = db.Column(
        db.Integer, 
        db.ForeignKey('hw_products.id'), 
        nullable=True
    )
    sw_id = db.Column(
        db.Integer, 
        db.ForeignKey('sw_products.id'), 
        nullable=True
    )
    crops_id = db.Column(
        db.Integer, 
        db.ForeignKey('crops.id'), 
        nullable=True
    )
    company_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    company_keywords = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )
    company_board_members = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    company_description = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    company_img = db.Column(
        db.String, 
        unique=False, 
        nullable=False
    )
    related_companies = db.Column(
        db.String, 
        unique=False,
        nullable=False
    )
    company_profits = db.Column(
        db.Text, 
        unique=False,
        nullable=False
    )
  
    def __init__(self, sw_id, hw_id, crops_id, company_name, company_keywords, company_board_members, company_description, company_img, related_companies, company_profits):
        self.sw_id = sw_id
        self.hw_id = hw_id
        self.crops_id = crops_id
        self.company_name = company_name
        self.company_keywords = company_keywords
        self.company_board_members = company_board_members
        self.company_description = company_description
        self.company_img = company_img
        self.related_companies = related_companies
        self.company_profits = company_profits

class MagickalInterventions(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'magickal_interventions'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    hw_id = db.Column(
        db.Integer, 
        db.ForeignKey('hw_products.id'), 
        nullable=True
    )
    sw_id = db.Column(
        db.Integer, 
        db.ForeignKey('sw_products.id'), 
        nullable=True
    )
    crops_id = db.Column(
        db.Integer, 
        db.ForeignKey('crops.id'), 
        nullable=True
    )
    company_id = db.Column(
        db.Integer, 
        db.ForeignKey('companies.id'), 
        nullable=True
    )
    spell_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    spell_type = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )
    spell_description = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    spell_code = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    spell_img = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=False
    )
    spell_locations = db.Column(
        db.String, 
        unique=False,
        nullable=False
    )
    spell_networks = db.Column(
        db.String, 
        unique=False,
        nullable=False
    )
    spell_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
    def __init__(self, sw_id, hw_id, crops_id, company_id, spell_name, spell_type, spell_description, spell_code, spell_img, spell_locations, spell_networks, spell_timestamp, user_id):
        self.sw_id = sw_id
        self.hw_id = hw_id
        self.crops_id = crops_id
        self.company_id = company_id
        self.spell_name = spell_name
        self.spell_type = spell_type
        self.spell_description = spell_description
        self.spell_code = spell_code
        self.spell_img = spell_img
        self.spell_locations = spell_locations
        self.spell_networks = spell_networks
        self.spell_timestamp = spell_timestamp
        self.user_id = user_id

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    spell_posts = db.relationship('MagickalInterventions', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username) 


