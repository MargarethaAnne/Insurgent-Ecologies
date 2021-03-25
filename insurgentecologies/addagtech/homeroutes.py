# pylint: disable=no-member
from flask import current_app as app
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, Blueprint, make_response, send_from_directory
import json
import os.path
from werkzeug.utils import secure_filename

from .forms import HWProductForm, SWProductForm

from datetime import datetime as dt
from .models import HWProducts, SWProducts, db

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='agtemplates',
    static_folder='agstatic'
)

@home_bp.route('/')
def home():
    return render_template('home.html')
    # return render_template('index.html', codes=session.keys())

@home_bp.route('/categories')
def categories():
    return render_template('categories-page.html')

@home_bp.route('/hardware')
def hardware():
    hardware_list = HWProducts.query.all()
    print(hardware_list)
    return render_template("hardware.html", hardware_list=hardware_list)

@home_bp.route('/software')
def software():
    software_list = SWProducts.query.all()
    print(software_list)
    return render_template("software.html", software_list=software_list)
   
@home_bp.route('/add-new-agtech')
def add_new():
    return render_template('add_options.html')

@home_bp.route('/add-new-hw')
def add_new_hw():
    form = HWProductForm()
    message=" "
    if form.validate_on_submit():
        return redirect(url_for("ag-tech-entry"))
    return render_template(
        "add_new_agtech.html",
        form=form,
        template="form-template",
        message=message
        )

@home_bp.route('/add-new-sw')
def add_new_sw():
    form = SWProductForm()
    message=" "
    if form.validate_on_submit():
        return redirect(url_for("ag-tech-entry-sw"))
    return render_template(
        "add_new_agtech_sw.html",
        form=form,
        template="form-template",
        message=message
        )

@home_bp.route('/ag-software-entry', methods=['GET', 'POST'])
def ag_software_entry():
    form = SWProductForm()
    # POST: 
    if request.method == 'POST':
        if form.is_submitted():
            print ("submitted")
        if form.validate():
            print ("valid")
            print(form.errors)
        if form.validate_on_submit():
            # Get Form Fields
            sw_company_name = request.form['sw_company_name']
            sw_company_product = request.form['sw_company_product']
            sw_software_components = request.form['sw_software_components']
            sw_categories = ', '.join(form.sw_categories.data)
            sw_product_description = request.form['sw_product_description']
            sw_product_img = request.files['sw_product_img']
            sw_os_license = request.form['sw_os_license']
            sw_references = request.form['sw_references']
            sw_locations_desc = request.form['sw_locations_desc']
            sw_locations_img = request.files['sw_locations_img']
            print (sw_categories)
            if 'sw_product_img' not in request.files:
                flash('No hw_product_img part')
            
            # filename = product_img.save(request.files['product_img'])
            # url = images.url(filename)
            
            # if user does not select file, browser also
            # submit an empty part without filename
            
            # if file.filename == '':
            #     flash('No selected file')
            #     return redirect(request.url)
            if sw_product_img:
                filename = secure_filename(sw_product_img.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                sw_product_img.save(os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename))
                sw_product_img_file = os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename)
            print (sw_product_img_file)

            if sw_locations_img:
                sw_l_filename = secure_filename(sw_locations_img.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                sw_locations_img.save(os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], sw_l_filename))
                sw_locations_img_file = os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], sw_l_filename)
            print (sw_locations_img_file)

            # existing_product = CompanyProducts.query.filter_by(company_product=company_product).first()
            # if existing_product:
            #     message = "This product has already been registered"
            #     return render_template('add_new_agtech.html', form=form, message=message)
            # if existing_product is None:
            sw_products = SWProducts(
                sw_company_name=sw_company_name, 
                sw_company_product=sw_company_product, 
                sw_software_components = sw_software_components,
                sw_categories = sw_categories,
                sw_product_description=sw_product_description, 
                sw_product_img=filename,
                sw_os_license=sw_os_license,
                sw_references=sw_references,
                sw_locations_desc = sw_locations_desc,
                sw_locations_img = sw_l_filename
                )

            db.session.add(sw_products)
            db.session.commit()
            flash('Record was successfully added')

            # GET: Serve Sign-up page
            return render_template(
                'software_entry.html',
                sw_products=sw_products
                )
        else:
            print("bad")
    return render_template('add_new_agtech_sw.html', form=form)


@home_bp.route('/ag-tech-entry', methods=['GET', 'POST'])
def ag_tech_entry():
    form = HWProductForm()
    # POST: 
    if request.method == 'POST':
        if form.is_submitted():
            print ("submitted")
        if form.validate():
            print ("valid")
        print(form.errors)
        if form.validate_on_submit():
            # Get Form Fields
            hw_company_name = request.form['hw_company_name']
            hw_company_product = request.form['hw_company_product']
            hw_hardware_components = request.form['hw_hardware_components']
            hw_categories = request.form['hw_categories']
            sw_id = request.form['sw_id']
            hw_product_description = request.form['hw_product_description']
            hw_product_img = request.files['hw_product_img']
            hw_references = request.form['hw_references']
            hw_locations_desc = request.form['hw_locations_desc']
            hw_locations_img = request.files['hw_locations_img']
            
            if 'hw_product_img' not in request.files:
                flash('No hw_product_img part')
            
            # filename = product_img.save(request.files['product_img'])
            # url = images.url(filename)
            
            # if user does not select file, browser also
            # submit an empty part without filename
            
            # if file.filename == '':
            #     flash('No selected file')
            #     return redirect(request.url)
            if hw_product_img:
                filename = secure_filename(hw_product_img.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                hw_product_img.save(os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename))
                hw_product_img_file = os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename)
            print (hw_product_img_file)

            if hw_locations_img:
                hw_l_filename = secure_filename(hw_locations_img.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                hw_locations_img.save(os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], hw_l_filename))
                hw_locations_img_file = os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], hw_l_filename)
            print (hw_locations_img_file)

            # existing_product = CompanyProducts.query.filter_by(company_product=company_product).first()
            # if existing_product:
            #     message = "This product has already been registered"
            #     return render_template('add_new_agtech.html', form=form, message=message)
            # if existing_product is None:
            hw_products = HWProducts(
                hw_company_name=hw_company_name, 
                hw_company_product=hw_company_product, 
                hw_hardware_components = hw_hardware_components,
                sw_id = sw_id,
                hw_categories = hw_categories,
                hw_product_description=hw_product_description, 
                hw_product_img=filename,
                hw_references=hw_references,
                hw_locations_desc = hw_locations_desc,
                hw_locations_img = hw_l_filename
                )

            db.session.add(hw_products)
            db.session.commit()
            flash('Record was successfully added')

            sw_product = SWProducts.query.filter_by(id=hw_products.sw_id).first_or_404()

            return render_template(
                'hardware_entry.html',
                hw_products=hw_products,
                sw_name=sw_product.sw_company_product
                )
        else:
            print("bad")
    return render_template('add_new_agtech.html', form=form)

@home_bp.route('/software/<int:id>')
def show_sw_entry(id):
    sw_products = SWProducts.query.filter_by(id=id).first_or_404()
    return render_template(
        'software_entry.html', 
        sw_products=sw_products
        )

@home_bp.route('/hardware/<int:id>')
def show_hw_entry(id):
    hw_products = HWProducts.query.filter_by(id=id).first_or_404()
    sw_id = SWProducts.query.filter_by(id=hw_products.sw_id).first_or_404()
    return render_template(
        'hardware_entry.html', 
        hw_products=hw_products,
        sw_id=sw_id
        )

@app.route('/user_files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_IMAGES_DEST'],
                               filename)    

@home_bp.route('/add-new-agtech/<string:company_product>')
def display(hw_company_product): 
    if os.path.exists('company_names.json'):
        with open('company_names.json') as company_names_file:
            company_names = json.load(company_names_file)
            if company_product in company_names.keys():
                if 'company_name' in company_names[company_product].keys():
                    return company_names[company_product]['company_name'], company_names[company_product]['company_name']['file']
 
    return abort(404)

@home_bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404