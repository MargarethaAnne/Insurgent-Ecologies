from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextField, TextAreaField, SubmitField, SelectField, widgets, SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from .models import SWProducts


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
    # sw_id = QuerySelectField(
    #     'Software',
    #     query_factory=lambda: SWProducts.query.all(),
    #     validators=[DataRequired()] 
    # )
    # sw_id = SelectField(
    #     'Software',
    #     choices = [(sw.id, sw.sw_company_product) for sw in SWProducts.query.all()],
    #     validators=[DataRequired()] 
    # )
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
            ('robot harvesters','robot harvesters')
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
    sw_id = SelectField(
        'Software Components', 
        choices = [(sw.id, sw.sw_company_product) for sw in SWProducts.query.all()]
        # coerce=int
        # validators=[DataRequired()] 
    )
    hw_locations_desc = StringField(
        'Locations (please separate by comma)',
        [DataRequired()]
    )
    hw_locations_img = FileField(
        'Location image',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
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

    # field = FieldType(
    # 'LABEL',
    # validators=[ExampleValidator(message="ERROR MESSAGE")],
    # )

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SWProductForm(FlaskForm):
    string_of_files = [
    'genomics', 'mapping', 'identification', 'analytics', 'statistics', 'NDVI', 'imagery', 'testing', 'marketing', 'supplychain', 'irrigation'
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
    # sw_company_product_id = SelectField(
    #     'Software Components', 
    #     choices=[],
    #     coerce=int,
    #     validators=[DataRequired()] 
    # )
    sw_locations_desc = StringField(
        'Locations (please separate by comma)',
        [DataRequired()]
    )
    sw_locations_img = FileField(
        'Location image',
        [DataRequired()]
        # validators=[FileRequired(), FileAllowed(images, 'Images only!')]
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

