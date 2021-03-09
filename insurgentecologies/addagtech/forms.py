from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length

class CompanyProductForm(FlaskForm):
    """Company Product Form."""
    company_name = StringField(
        'Company Name',
        [DataRequired()]
    )
    company_product = StringField(
        'Company Product',
        [DataRequired()]
    )
    img_url = StringField(
        'Image Url',
        [DataRequired()]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

    # field = FieldType(
    # 'LABEL',
    # validators=[ExampleValidator(message="ERROR MESSAGE")],
    # )