from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, widgets, SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets.core import html_params
from markupsafe import Markup
from .models import HWProducts, SWProducts, Crops, Companies, MagickalInterventions
import pycountry

class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country.name, country.name) for country in pycountry.countries]


class CustomSelect:
    """
    Renders a select field allowing custom attributes for options.
    Expects the field to be an iterable object of Option fields.
    The render function accepts a dictionary of option ids ("{field_id}-{option_index}")
    which contain a dictionary of attributes to be passed to the option.

    Example:
    form.customselect(option_attr={"customselect-0": {"disabled": ""} })
    """

    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, option_attr=None, **kwargs):
        if option_attr is None:
            option_attr = {}
        kwargs.setdefault("id", field.id)
        if self.multiple:
            kwargs["multiple"] = True
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True
        html = ["<select %s>" % html_params(name=field.name, **kwargs)]
        for option in field:
            attr = option_attr.get(option.id, {})
            html.append(option(**attr))
        html.append("</select>")
        return Markup("".join(html))

class HWProductForm(FlaskForm):
    """Company Product Form."""
    hw_company_name = StringField(
        'Company Name',
        [DataRequired()]
    )
    hw_company_product = StringField(
        'Company Product',
        [DataRequired()]
    )
    hw_hardware_components = StringField(
        'Hardware Components (please separate by comma)',
        [DataRequired()]
    )
    hw_categories = SelectField(
        'Category', 
        choices=[
            ('robot seeders and planters','robot seeders and planters'), 
            ('precision technology','precision technology'),
            ('cybernetic greenhouses','cybernetic greenhouses'),
            ('irrigation','irrigation'),
            ('pesticide and fertilizer robots','pesticide and fertilizer robots'),
            ('sensors','sensors'),
            ('herd management', 'herd management'),
            ('robot harvesters','robot harvesters'),
            ('other','other')
            ],
        validators=[DataRequired()] 
    )
    hw_product_description = TextAreaField(
        'Product Description',
        [DataRequired()]
    )
    hw_product_img = FileField(
        'Product Image',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    hw_references = StringField(
        'References (links - please separate by comma)',
        [DataRequired()]
    )
    sw_id = QuerySelectField(
        'Software used', 
        query_factory=lambda: SWProducts.query.all(),
        get_label='sw_company_product',
        allow_blank=True,
        # widget=CustomSelect(),
    )
    hw_locations_desc = CountrySelectField(
        'Locations (please separate by comma)',
        [DataRequired()]
    )
    hw_locations_img = FileField(
        'Location image',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    crops_id = QuerySelectField(
        'Related Crops', 
        query_factory=lambda: Crops.query.all(),
        get_label='crop_name',
        allow_blank=True
    )
    # spells_id = StringField(
    #     'Spells (select one)'
    # )

    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

    # field = FieldType(
    # 'LABEL',
    # validators=[ExampleValidator(message="ERROR MESSAGE")],
    # )

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SWProductForm(FlaskForm):
    string_of_files = [
    'genomics', 'mapping', 'identification', 'analytics', 'statistics', 'NDVI', 'imagery', 'testing', 'marketing', 'supplychain', 'irrigation', 'other'
    ]
    
    files = [(x, x) for x in string_of_files]

    """Software Product Form."""
    sw_company_name = StringField(
        'Company Name',
        [DataRequired()]
    )
    sw_company_product = StringField(
        'Company Product',
        [DataRequired()]
    )
    sw_software_components = StringField(
        'Software Elements (please separate by comma)',
        [DataRequired()]
    )
    sw_categories = MultiCheckboxField(
        'Category', 
        choices=files
    )
    sw_product_description = TextAreaField(
        'Product Description',
        [DataRequired()]
    )
    sw_product_img = FileField(
        'Product Image',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    sw_os_license = StringField(
        'Add Open Source License if applicable',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    sw_references = StringField(
        'References (links - please separate by comma)',
        [DataRequired()]
    )

    sw_locations_desc = CountrySelectField(
        'Locations (please separate by comma)',
        [DataRequired()]
    )
    sw_locations_img = FileField(
        'Location image',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    crops_id = QuerySelectField(
        'Related Crops', 
        query_factory=lambda: Crops.query.all(),
        get_label='crop_name',
        allow_blank=True
    )
    # crops_id = MultiCheckboxField(
    #     'Crops (check all that apply)',
    #     coerce=int,
    #     validators=[DataRequired()]
    # )
    # spells_id = StringField(
    #     'Spells (select one)'
    # )

    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')



class CropForm(FlaskForm):

    """crops form entry"""
    crop_name = StringField(
        'Crop Name',
        [DataRequired()]
    )
    genus_species = StringField(
        'Genus species',
        [DataRequired()]
    )
    crop_intellectual_property = StringField(
        'Intellectual property data',
        [DataRequired()]
    )
    crop_chemicals_used = StringField(
        'Chemicals used',
        [DataRequired()]
    )
    sw_id = QuerySelectField(
        'Software used', 
        query_factory=lambda: SWProducts.query.all(),
        get_label='sw_company_product',
        allow_blank=True
    )
    hw_id = QuerySelectField(
        'Hardware used', 
        query_factory=lambda: HWProducts.query.all(),
        get_label='hw_company_product',
        allow_blank=True
    )
    company_id = QuerySelectField(
        'Related Companies', 
        query_factory=lambda: Companies.query.all(),
        get_label='company_name',
        allow_blank=True
    )
    crop_genetic_information = TextAreaField(
        'Genetic Information',
        [DataRequired()]
    )
    crop_companions = StringField(
        'Companions',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    crop_description = StringField(
        'Description',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    crop_img = FileField(
        'Crop image',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    crop_references = StringField(
        'References (links - please separate by comma)',
        [DataRequired()]
    )
    # sw_company_product_id = SelectField(
    #     'Software Components', 
    #     choices=[],
    #     coerce=int,
    #     validators=[DataRequired()] 
    # )
    crop_locations = CountrySelectField(
        'Locations grown',
    )

    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


class CompanyForm(FlaskForm):

    """company form entry"""
    company_name = StringField(
        'Company Name',
        [DataRequired()]
    )
    company_keywords = StringField(
        'Keywords',
    )
    company_board_members = StringField(
        'Board members',
        [DataRequired()]
    )
    company_description = TextAreaField(
        'Company description',
        [DataRequired()]
    )
    company_img = FileField(
        'Company image',
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    hw_id = QuerySelectField(
        'Related Hardware', 
        query_factory=lambda: HWProducts.query.all(),
        get_label='hw_company_product',
        allow_blank=True
    )
    sw_id = QuerySelectField(
        'Related Software', 
        query_factory=lambda: SWProducts.query.all(),
        get_label='sw_company_product',
        allow_blank=True
    )
    crops_id = QuerySelectField(
        'Related Crops', 
        query_factory=lambda: SWProducts.query.all(),
        get_label='sw_company_product',
        allow_blank=True
    )
    related_companies = StringField(
        'Related Companies',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    company_profits = StringField(
        'Company Profits',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )

    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


class MagickalInterventionForm(FlaskForm):
    string_of_files = [
    'hex', 'curse', 'spell', 'ritual', 'brew', 'seed', 'invocation', 'incantation', 'necromancy', 'ancestor work', 'other'
    ]
    files = [(x, x) for x in string_of_files]
    """crops form entry"""
    hw_id = QuerySelectField(
        'Related Hardware', 
        query_factory=lambda: HWProducts.query.all(),
        get_label='hw_company_product',
        allow_blank=True
    )
    sw_id = QuerySelectField(
        'Related Software', 
        query_factory=lambda: SWProducts.query.all(),
        get_label='sw_company_product',
        allow_blank=True
    )
    crops_id = QuerySelectField(
        'Related Crops', 
        query_factory=lambda: Crops.query.all(),
        get_label='crop_name',
        allow_blank=True
    )
    company_id = QuerySelectField(
        'Related Company', 
        query_factory=lambda: Companies.query.all(),
        get_label='company_name',
        allow_blank=True
    )
    spell_name = StringField(
        'Name of Magickal Intervention',
        [DataRequired()]
    )
    spell_type = MultiCheckboxField(
        'Type of magickal intervention',
        choices=files
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    spell_description = TextAreaField(
        'Spell description',
        [DataRequired()]
    )
    spell_code = TextAreaField(
        'Spell code',
        [DataRequired()]
    )
    spell_img = FileField(
        'Company image',
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    spell_locations = CountrySelectField(
        'Locations for Magickal Intervention',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )
    spell_networks = StringField(
        'Covens and other connections',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
    )

    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')