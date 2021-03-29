# pylint: disable=no-member
from flask import current_app as app
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, Blueprint, make_response, send_from_directory
import json
import os.path
from werkzeug.utils import secure_filename

from .forms import HWProductForm, SWProductForm, CropForm, CompanyForm, MagickalInterventionForm

from datetime import datetime as dt
from .models import HWProducts, SWProducts, Crops, Companies, MagickalInterventions, db

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

@home_bp.route('/crops')
def crops():
    crop_list = Crops.query.all()
    print(crop_list)
    return render_template("crops.html", crop_list=crop_list)

@home_bp.route('/companies')
def companies():
    company_list = Companies.query.all()
    print(company_list)
    return render_template("companies.html", company_list=company_list)

@home_bp.route('/magickal-interventions')
def magickal_interventions():
    spells_list = MagickalInterventions.query.all()
    print(spells_list)
    return render_template("magickal-interventions.html", spells_list=spells_list)
   
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
    print("here we are")
    message=" "
    if form.validate_on_submit():
        print("valid")
        return redirect(url_for("ag-software-entry"))
    print("not valid")
    return render_template(
        "add_new_agtech_sw.html",
        form=form,
        template="form-template",
        message=message
        )

@home_bp.route('/add-new-crop')
def add_new_crop():
    form = CropForm()
    message=" "
    if form.validate_on_submit():
        return redirect(url_for("crop-entry"))
    return render_template(
        "add_new_crop.html",
        form=form,
        template="form-template",
        message=message
        )
@home_bp.route('/add-new-company')
def add_new_company():
    form = CompanyForm()
    message=" "
    if form.validate_on_submit():
        return redirect(url_for("ag-company-entry"))
    return render_template(
        "add_new_company.html",
        form=form,
        template="form-template",
        message=message
        )
@home_bp.route('/add-magickal-intervention')
def add_magickal_intervention():
    form = MagickalInterventionForm()
    message=" "
    if form.validate_on_submit():
        return redirect(url_for("magickal-entry"))
    return render_template(
        "add_new_magickal_intervention.html",
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
            sw_locations_desc = form.sw_locations_desc.data
            sw_locations_img = request.files['sw_locations_img']
            crops_id = request.form['crops_id']

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
                sw_locations_img = sw_l_filename,
                crops_id = crops_id
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
            hw_locations_desc = ', '.join(form.hw_locations_desc.data)
            hw_locations_img = request.files['hw_locations_img']
            crops_id = request.form['crops_id']
            
            if 'hw_product_img' not in request.files:
                flash('No hw_product_img part')

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
                hw_locations_img = hw_l_filename,
                crops_id = crops_id
                )

            db.session.add(hw_products)
            db.session.commit()
            flash('Record was successfully added')

            sw_id = SWProducts.query.filter_by(id=hw_products.sw_id).first_or_404()

            return render_template(
                'hardware_entry.html',
                hw_products=hw_products,
                sw_id=sw_id
                )
        else:
            print("bad")
    return render_template('add_new_agtech.html', form=form)

@home_bp.route('/crop-entry', methods=['GET', 'POST'])
def crop_entry():
    form = CropForm()
    # POST: 
    if request.method == 'POST':
        if form.is_submitted():
            print ("submitted")
        if form.validate():
            print ("valid")
        print(form.errors)
        if form.validate_on_submit():
            # Get Form Fields
            crop_name = request.form['crop_name']
            genus_species = request.form['genus_species']
            crop_intellectual_property = request.form['crop_intellectual_property']
            crop_chemicals_used = request.form['crop_chemicals_used']
            sw_id = request.form['sw_id']
            hw_id = request.form['hw_id']
            company_id = request.form['company_id']
            crop_genetic_information = request.form['crop_genetic_information']
            crop_companions = request.form['crop_companions']
            crop_description = request.form['crop_description']
            crop_img = request.files['crop_img']
            crop_references = request.form['crop_references']
            crop_locations = ', '.join(form.crop_locations.data)
            
            if 'crop_img' not in request.files:
                flash('No crop image')

            if crop_img:
                filename = secure_filename(crop_img.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                crop_img.save(os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename))
                crop_img_file = os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename)
            print (crop_img_file)

            crops = Crops(
                crop_name=crop_name, 
                genus_species=genus_species, 
                crop_intellectual_property = crop_intellectual_property,
                crop_chemicals_used = crop_chemicals_used,
                sw_id = sw_id,
                hw_id = hw_id,
                company_id = company_id,
                crop_genetic_information = crop_genetic_information,
                crop_companions=crop_companions, 
                crop_description=crop_description,
                crop_img=filename,
                crop_references=crop_references,
                crop_locations = crop_locations
                )

            db.session.add(crops)
            db.session.commit()
            flash('Record was successfully added')

            sw_id = SWProducts.query.filter_by(id=crops.sw_id).first_or_404()
            hw_id = HWProducts.query.filter_by(id=crops.hw_id).first_or_404()
            company_id = Companies.query.filter_by(id=crops.company_id).first_or_404()

            return render_template(
                'crop_entry.html',
                crops=crops,
                sw_id=sw_id,
                hw_id=hw_id,
                company_id=company_id
                )
        else:
            print("bad")
    return render_template('add_new_crop.html', form=form)

@home_bp.route('/ag-company-entry', methods=['GET', 'POST'])
def ag_company_entry():
    form = CompanyForm()
    # POST: 
    if request.method == 'POST':
        if form.is_submitted():
            print ("submitted")
        if form.validate():
            print ("valid")
        print(form.errors)
        if form.validate_on_submit():
            # Get Form Fields
            sw_id = request.form['sw_id']
            hw_id = request.form['hw_id']
            crops_id = request.form['crops_id']
            company_name = request.form['company_name']
            company_keywords = request.form['company_keywords']
            company_board_members = request.form['company_board_members']
            company_description = request.form['company_description']
            company_img = request.files['company_img']
            related_companies = request.form['related_companies']
            company_profits = request.form['company_profits']
            
            if 'company_img' not in request.files:
                flash('No company image')

            if company_img:
                filename = secure_filename(company_img.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                company_img.save(os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename))
                company_img_file = os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename)
            print (company_img_file)

            companies = Companies(
                sw_id=sw_id, 
                hw_id=hw_id, 
                crops_id = crops_id,
                company_name = company_name,
                company_keywords = company_keywords,
                company_board_members = company_board_members,
                company_description = company_description,
                company_img=filename, 
                related_companies=related_companies,
                company_profits=company_profits
                )

            db.session.add(companies)
            db.session.commit()
            flash('Record was successfully added')

            sw_id = SWProducts.query.filter_by(id=companies.sw_id).first_or_404()
            hw_id = HWProducts.query.filter_by(id=companies.hw_id).first_or_404()
            crops_id = Crops.query.filter_by(id=companies.crops_id).first_or_404()

            return render_template(
                'company_entry.html',
                companies=companies,
                sw_id=sw_id,
                hw_id=hw_id,
                crops_id=crops_id
                )
        else:
            print("bad")
    return render_template('add_new_crop.html', form=form)


@home_bp.route('/magickal-entry', methods=['GET', 'POST'])
def magickal_entry():
    form = MagickalInterventionForm()
    # POST: 
    if request.method == 'POST':
        if form.is_submitted():
            print ("submitted")
        if form.validate():
            print ("valid")
        print(form.errors)
        if form.validate_on_submit():
            # Get Form Fields
            hw_id = request.form['hw_id']
            sw_id = request.form['sw_id']
            crops_id = request.form['crops_id']
            company_id = request.form['company_id']
            spell_name = request.form['spell_name']
            spell_type = request.form['spell_type']
            spell_description = request.form['spell_description']
            spell_code = request.form['spell_code']
            spell_img = request.files['spell_img']
            spell_locations = ', '.join(form.spell_locations.data)
            spell_networks = request.form['spell_networks']
            
            if 'spell_img' not in request.files:
                flash('No spell image')

            if spell_img:
                filename = secure_filename(spell_img.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                spell_img.save(os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename))
                spell_img_file = os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename)
            print (spell_img_file)

            magickal_interventions = MagickalInterventions(
                hw_id=hw_id, 
                sw_id=sw_id, 
                crops_id = crops_id,
                company_id = company_id,
                spell_name = spell_name,
                spell_type = spell_type,
                spell_description = spell_description,
                spell_code = spell_code, 
                spell_img = filename,
                spell_locations=spell_locations,
                spell_networks=spell_networks
                )

            db.session.add(magickal_interventions)
            db.session.commit()
            flash('Record was successfully added')

            sw_id = SWProducts.query.filter_by(id=magickal_interventions.sw_id).first_or_404()
            hw_id = HWProducts.query.filter_by(id=magickal_interventions.hw_id).first_or_404()
            crops_id = Crops.query.filter_by(id=magickal_interventions.crops_id).first_or_404()
            company_id = Companies.query.filter_by(id=magickal_interventions.crops_id).first_or_404()

            return render_template(
                'magickal-entry.html',
                magickal_interventions=magickal_interventions,
                sw_id=sw_id,
                hw_id=hw_id,
                crops_id=crops_id,
                company_id=company_id
                )
        else:
            print("bad")
    return render_template('add_new_magickal_intervention.html', form=form)

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

@home_bp.route('/crops/<int:id>')
def show_crop_entry(id):
    crops = Crops.query.filter_by(id=id).first_or_404()
    sw_id = SWProducts.query.filter_by(id=crops.sw_id).first_or_404()
    hw_id = HWProducts.query.filter_by(id=crops.hw_id).first_or_404()
    company_id = Companies.query.filter_by(id=crops.company_id).first_or_404()

    return render_template(
        'crop_entry.html', 
        crops=crops,
        sw_id=sw_id,
        hw_id=hw_id,
        company_id=company_id
        )

@home_bp.route('/companies/<int:id>')
def show_company_entry(id):
    companies = Companies.query.filter_by(id=id).first_or_404()
    sw_id = SWProducts.query.filter_by(id=companies.sw_id).first_or_404()
    hw_id = HWProducts.query.filter_by(id=companies.hw_id).first_or_404()
    crops_id = Crops.query.filter_by(id=companies.crops_id).first_or_404()
    return render_template(
        'company_entry.html', 
        companies=companies,
        sw_id=sw_id,
        hw_id=hw_id,
        crops_id=crops_id
        )
@home_bp.route('/magickal-interventions/<int:id>')
def show_magickal_intervention(id):
    magickal_interventions = MagickalInterventions.query.filter_by(id=id).first_or_404()

    sw_id = SWProducts.query.filter_by(id=magickal_interventions.sw_id).first_or_404()
    hw_id = HWProducts.query.filter_by(id=magickal_interventions.hw_id).first_or_404()
    crops_id = Crops.query.filter_by(id=magickal_interventions.crops_id).first_or_404()
    company_id = Companies.query.filter_by(id=magickal_interventions.crops_id).first_or_404()

    return render_template(
        'magickal-entry.html', 
        magickal_interventions=magickal_interventions,
        sw_id=sw_id,
        hw_id=hw_id,
        crops_id=crops_id,
        company_id=company_id
        )

@app.route('/user_files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_IMAGES_DEST'],
                               filename)    

@home_bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404