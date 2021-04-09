"""Data models."""
# pylint: disable=no-member
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import MetaData
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import backref

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

crops_companies = db.Table('crops_companies',
    db.Column('crops_id', db.Integer, db.ForeignKey('crops.id')),
    db.Column('companies_id', db.Integer,db.ForeignKey('companies.id'))
    )

crops_software = db.Table('crops_software',
    db.Column('crops_id', db.Integer, db.ForeignKey('crops.id')),
    db.Column('software_id', db.Integer,db.ForeignKey('sw_products.id'))
    )

crops_hardware = db.Table('crops_hardware',
    db.Column('crops_id', db.Integer, db.ForeignKey('crops.id')),
    db.Column('hardware_id', db.Integer,db.ForeignKey('hw_products.id'))
    )

companies_software = db.Table('companies_software',
    db.Column('companies_id', db.Integer, db.ForeignKey('companies.id')),
    db.Column('software_id', db.Integer,db.ForeignKey('sw_products.id'))
    )

companies_hardware = db.Table('companies_hardware',
    db.Column('companies_id', db.Integer, db.ForeignKey('companies.id')),
    db.Column('hardware_id', db.Integer,db.ForeignKey('hw_products.id'))
    )

software_hardware = db.Table('software_hardware',
    db.Column('software_id', db.Integer, db.ForeignKey('sw_products.id')),
    db.Column('hardware_id', db.Integer,db.ForeignKey('hw_products.id'))
    )
software_sw_categories = db.Table('software_sw_categories',
    db.Column('software_id', db.Integer, db.ForeignKey('sw_products.id')),
    db.Column('sw_categories_id', db.Integer, db.ForeignKey('sw_categories.id'))
    )
hardware_hw_categories = db.Table('hardware_hw_categories',
    db.Column('hardware_id', db.Integer, db.ForeignKey('hw_products.id')),
    db.Column('hw_categories_id', db.Integer, db.ForeignKey('hw_categories.id'))
    )

class SWCategories(db.Model):
    __tablename__='sw_categories'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    sw_categories_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    catsoft_connections = db.relationship('SWProducts', 
    secondary=software_sw_categories, 
    back_populates='softcat_connections')

class HWCategories(db.Model):
    __tablename__='hw_categories'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    hw_categories_name = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    cathard_connections = db.relationship('HWProducts', 
    secondary=hardware_hw_categories, 
    back_populates='hardcat_connections')

class HWProducts(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'hw_products'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    # sw_id = db.Column(
    #     db.Integer, 
    #     db.ForeignKey('sw_products.id'), 
    #     nullable=True
    #     )
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
    # hw_categories = db.Column(
    #     db.String(80),
    #     index=True,
    #     unique=False,
    #     nullable=False
    # )
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
    #     db.ForeignKey('crops.id'), 
    #     nullable=True
    # )

    hardcrop_connections = db.relationship('Crops', 
        secondary=crops_hardware, 
        back_populates='crophard_connections')

    hc_connections = db.relationship('Companies', 
        secondary=companies_hardware, 
        back_populates='ch_connections')

    hardsoft_connections = db.relationship('SWProducts', 
        secondary=software_hardware, 
        back_populates='softhard_connections')

    hardcat_connections = db.relationship('HWCategories', 
        secondary=hardware_hw_categories, 
        back_populates='cathard_connections')

    author = db.relationship('User', back_populates='hw_posts')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
    def __init__(self, hw_company_name, hw_company_product, hw_hardware_components, hw_product_description, hw_product_img, hw_references, hw_locations_desc, hw_locations_img, user_id):
        # self.sw_id=sw_id
        self.hw_company_name = hw_company_name
        self.hw_company_product = hw_company_product
        self.hw_hardware_components = hw_hardware_components
        # self.hw_categories = hw_categories
        self.hw_product_description = hw_product_description
        self.hw_product_img = hw_product_img
        # self.sw_company_product = sw_company_product
        self.hw_locations_desc = hw_locations_desc
        self.hw_locations_img = hw_locations_img
        self.hw_references = hw_references
        # self.crops_id = crops_id
        self.user_id = user_id
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
    # sw_categories = db.Column(
    #     db.Text,
    #     index=False,
    #     unique=False,
    #     nullable=False
    # )
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
  
    softcat_connections = db.relationship('SWCategories', 
        secondary=software_sw_categories, 
        back_populates='catsoft_connections')
    
    softcomp_connections = db.relationship('Companies', 
        secondary=companies_software, 
        back_populates='compsoft_connections')

    softcrop_connections = db.relationship('Crops', 
        secondary=crops_software, 
        back_populates='cropsoft_connections')

    softhard_connections = db.relationship('HWProducts', 
        secondary=software_hardware, 
        back_populates='hardsoft_connections')

    # crop_to_software = db.relationship('Crops', back_populates='software_to_crop')
    author = db.relationship('User', back_populates='sw_posts')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
    def __init__(self, sw_company_name, sw_company_product, sw_software_components, sw_product_description, sw_product_img, sw_os_license, sw_references, sw_locations_desc, sw_locations_img, user_id):
        self.sw_company_name = sw_company_name
        self.sw_company_product = sw_company_product
        self.sw_software_components = sw_software_components
        self.sw_product_description = sw_product_description
        self.sw_product_img = sw_product_img
        self.sw_os_license = sw_os_license
        self.sw_locations_desc = sw_locations_desc
        self.sw_locations_img = sw_locations_img
        self.sw_references = sw_references
        # self.crops_id = crops_id
        self.user_id = user_id
        print(repr(self.sw_company_name))
        print(repr(self.sw_company_product))
        print(repr(self.sw_product_img))
        tellme=type(self.sw_company_name)
        print(tellme)
        
# crops_companies_assoc = db.Table('crops_companies_assoc', db.Model.metadata,
#     db.Column('crops_id', db.Integer, db.ForeignKey('crops.id')),
#     db.Column('companies_id', db.Integer, db.ForeignKey('companies.id'))
# )
class Crops(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'crops'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    # hw_id = db.Column(
    #     db.Integer, 
    #     db.ForeignKey('hw_products.id'), 
    #     nullable=True
    # )
    # sw_id = db.Column(
    #     db.Integer, 
    #     db.ForeignKey('sw_products.id'), 
    #     nullable=True
    # )
    # company_id = db.Column(
    #     db.Integer, 
    #     db.ForeignKey('companies.id'), 
    #     nullable=True
    # )
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

    cropcomp_connections = db.relationship('Companies', 
        secondary=crops_companies, 
        back_populates='compcrop_connections')

    cropsoft_connections = db.relationship('SWProducts', 
        secondary=crops_software, 
        back_populates='softcrop_connections')
    
    crophard_connections = db.relationship('HWProducts', 
        secondary=crops_hardware, 
        back_populates='hardcrop_connections')

    # one to many relationship:
    author = db.relationship('User', back_populates='crops_posts')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # crops_children = db.relationship(
    #     "Companies",
    #     secondary=crops_companies_assoc,
    #     back_populates="companies_parents")
  
    def __init__(self, crop_name, genus_species, crop_intellectual_property, crop_chemicals_used, crop_genetic_information, crop_companions, crop_description, crop_img, crop_references, crop_locations, user_id):
        # self.hw_id = hw_id
        # self.sw_id = sw_id
        # self.company_id = company_id
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
        self.user_id = user_id


class Companies(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'companies'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    # hw_id = db.Column(
    #     db.Integer, 
    #     db.ForeignKey('hw_products.id'), 
    #     nullable=True
    # )
    # sw_id = db.Column(
    #     db.Integer, 
    #     db.ForeignKey('sw_products.id'), 
    #     nullable=True
    # )
    # crops_id = db.Column(
    #     db.Integer, 
    #     db.ForeignKey('crops.id'), 
    #     nullable=True
    # )
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

    compcrop_connections = db.relationship('Crops', 
        secondary=crops_companies, 
        back_populates='cropcomp_connections')

    compsoft_connections = db.relationship('SWProducts', 
        secondary=companies_software, 
        back_populates='softcomp_connections')

    ch_connections = db.relationship('HWProducts', 
        secondary=companies_hardware, 
        back_populates='hc_connections')

    #one to many relationship:
    author = db.relationship('User', back_populates='company_posts')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # companies_parents = db.relationship(
    #     "Crops",
    #     secondary=crops_companies_assoc,
    #     back_populates="crops_children")
  
    def __init__(self, company_name, company_keywords, company_board_members, company_description, company_img, related_companies, company_profits, user_id):
        # self.sw_id = sw_id
        # self.hw_id = hw_id
        # self.crops_id = crops_id
        self.company_name = company_name
        self.company_keywords = company_keywords
        self.company_board_members = company_board_members
        self.company_description = company_description
        self.company_img = company_img
        self.related_companies = related_companies
        self.company_profits = company_profits
        self.user_id = user_id


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
    spell_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship('User', back_populates='spell_posts')
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

#many to many between history and locations:

history_locations = db.Table('history_locations',
    db.Column('history_id', db.Integer, db.ForeignKey('history.id')),
    db.Column('locations_id', db.Integer,db.ForeignKey('locations.id'))
    )

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    history_name = db.Column(db.String(30), index=False, unique=False)
    author = db.relationship('User', back_populates='history_posts')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hl_connections = db.relationship('Locations', 
    secondary=history_locations, 
    back_populates='lh_connections')
    
    # def __init__(self, history_name, user_id):
    #     self.history_name = history_name
    #     self.user_id = user_id

class Locations(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(30), index=False, unique=False)
    author = db.relationship('User', back_populates='locations_posts')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lh_connections = db.relationship('History', 
    secondary=history_locations, 
    back_populates='hl_connections')

    # def __init__(self, location_name, user_id):
    #     self.location_name = location_name
    #     self.user_id = user_id

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    history_posts = db.relationship('History', back_populates='author')
    locations_posts = db.relationship('Locations', back_populates='author')
    spell_posts = db.relationship('MagickalInterventions', back_populates='author')
    company_posts = db.relationship('Companies', back_populates='author')
    crops_posts = db.relationship('Crops', back_populates='author')
    sw_posts = db.relationship('SWProducts', back_populates='author')
    hw_posts = db.relationship('HWProducts', back_populates='author')

    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username) 
    
    def __init__(self, username, email, last_seen):
        self.username = username
        self.email = email
        self.last_seen = last_seen



