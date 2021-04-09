from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, widgets, SelectMultipleField, PasswordField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from wtforms.widgets.core import html_params
from markupsafe import Markup
from .models import HWProducts, SWProducts, Crops, Companies, MagickalInterventions, User, History, Locations, HWCategories, SWCategories
import pycountry

class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country.name, country.name) for country in pycountry.countries]

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput() 

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
    # sw_choices = []
    # for softwares in SWProducts.query.all():
    #     sw_choices.append((softwares.sw_company_name, softwares.sw_company_name))

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
    # hw_categories = SelectField(
    #     'Category', 
    #     choices=[
    #         ('robot seeders and planters','robot seeders and planters'), 
    #         ('precision technology','precision technology'),
    #         ('cybernetic greenhouses','cybernetic greenhouses'),
    #         ('irrigation','irrigation'),
    #         ('pesticide and fertilizer robots','pesticide and fertilizer robots'),
    #         ('sensors','sensors'),
    #         ('herd management', 'herd management'),
    #         ('robot harvesters','robot harvesters'),
    #         ('other','other')
    #         ],
    #     validators=[DataRequired()] 
    # )

    hw_categories = QuerySelectMultipleField(
        'Categories', 
        query_factory=lambda: HWCategories.query.order_by(HWCategories.id).all(),
        get_label='hw_categories_name',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=True
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

    sw_id = QuerySelectMultipleField(
        'Software used', 
        query_factory=lambda: SWProducts.query.order_by(SWProducts.id).all(),
        get_label='sw_company_product',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=True
        )

    companies_list = QuerySelectMultipleField(
        'Associated Companies', 
        query_factory=lambda: Companies.query.order_by(Companies.id).all(),
        get_label='company_name',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=True
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
    crops_id = QuerySelectMultipleField(
        'Related Crops', 
        query_factory=lambda: Crops.query.order_by(Crops.id).all(),
        get_label='crop_name',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
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

# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()

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
    crops_id = QuerySelectMultipleField(
        'Related Crops', 
        query_factory=lambda: Crops.query.order_by(Crops.id).all(),
        get_label='crop_name',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=True
    )
    hw_id = QuerySelectMultipleField(
        'Related Hardware', 
        query_factory=lambda: HWProducts.query.order_by(HWProducts.id).all(),
        get_label='hw_company_product',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=True
        )

    companies_list = QuerySelectMultipleField(
        'Associated Companies', 
        query_factory=lambda: Companies.query.order_by(Companies.id).all(),
        get_label='company_name',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=True
    )

    sw_categories = QuerySelectMultipleField(
        'Categories', 
        query_factory=lambda: SWCategories.query.order_by(SWCategories.id).all(),
        get_label='sw_categories_name',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=True
    )


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
    # sw_id = QuerySelectField(
    #     'Software used', 
    #     query_factory=lambda: SWProducts.query.all(),
    #     get_label='sw_company_product',
    #     allow_blank=True
    # )
    sw_id = QuerySelectMultipleField(
        'Related Software', 
        query_factory=lambda: SWProducts.query.order_by(SWProducts.id).all(),
        get_label='sw_company_product',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=True
    )
    hw_id = QuerySelectMultipleField(
        'Related Hardware', 
        query_factory=lambda: HWProducts.query.order_by(HWProducts.id).all(),
        get_label='hw_company_product',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=True
    )
    companies_list = QuerySelectMultipleField(
        'Associated Companies', 
        query_factory=lambda: Companies.query.order_by(Companies.id).all(),
        get_label='company_name',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
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
    sw_id = QuerySelectMultipleField(
        'Related Software', 
        query_factory=lambda: SWProducts.query.order_by(SWProducts.id).all(),
        get_label='sw_company_product',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=True
    )
    hw_id = QuerySelectMultipleField(
        'Related Hardware', 
        query_factory=lambda: HWProducts.query.order_by(HWProducts.id).all(),
        get_label='hw_company_product',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
        allow_blank=True
    )
    crops_id = QuerySelectMultipleField(
        'Related Crops', 
        query_factory=lambda: Crops.query.order_by(Crops.id).all(),
        get_label='crop_name',
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False), 
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

class LocationForm(FlaskForm):
    location_name = StringField(
        'Name of Location',
        [DataRequired()]
    )
    history_list = QuerySelectField(
        'history',
        query_factory=lambda: History.query.all(),
        get_label='history_name',
        allow_blank=True
        )
    
    submit = SubmitField('Submit')

class HistoryForm(FlaskForm):
    history_name = StringField(
        'Name of History',
        [DataRequired()]
    )
    locations_list = QuerySelectField(
        'locations',
        query_factory=lambda: Locations.query.all(),
        get_label='location_name',
        allow_blank=True
        )
    
    submit = SubmitField('Submit')

class SWCategoryForm(FlaskForm):
    sw_categories_name = StringField(
        'Name of Software Category',
        [DataRequired()]
    )
    submit = SubmitField('Submit')

class HWCategoryForm(FlaskForm):
    hw_categories_name = StringField(
        'Name of Hardware Category',
        [DataRequired()]
    )
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')