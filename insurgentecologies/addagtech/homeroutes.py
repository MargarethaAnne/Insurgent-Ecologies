# pylint: disable=no-member
from flask import current_app as app
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, Blueprint, make_response, send_from_directory, g
import json
import os.path
from werkzeug.utils import secure_filename
from flask import request
from werkzeug.urls import url_parse

from flask_login import current_user, login_user, logout_user, login_required
from .forms import HWProductForm, SWProductForm, CropForm, CompanyForm, MagickalInterventionForm, RegistrationForm, LoginForm, EditProfileForm, LocationForm, HistoryForm, HWCategoryForm, SWCategoryForm

from datetime import datetime as dt
from .models import HWProducts, SWProducts, Crops, Companies, MagickalInterventions, User, db, History, Locations, history_locations, software_hardware, crops_hardware, companies_hardware, crops_software, companies_software, crops_companies, hardware_hw_categories, software_sw_categories, HWCategories, SWCategories
from flask_login import LoginManager
from datetime import datetime

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='agtemplates',
    static_folder='agstatic'
)

# from addagtech import login

# @app.shell_context_processor
# def make_shell_context():
#     return {'db':db,'User':User}

login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):

    return User.query.get(int(id))

@home_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, last_seen=datetime.utcnow())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('home_bp.log_in'))
    return render_template('register.html', title='Register', form=form)

@home_bp.route('/login', methods=['GET', 'POST'])
def log_in():
    print("herewe are")
    if current_user.is_authenticated:
        print("logged in")
        return redirect(url_for('home_bp.home'))
    form = LoginForm()
    print("herewe are")
    if form.validate_on_submit():
        print("valid")
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('home_bp.log_in'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home_bp.home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@home_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_bp.home'))

@home_bp.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@home_bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    users = User.query.all()
    spell_posts = user.spell_posts
    company_posts = user.company_posts
    crops_posts = user.crops_posts
    sw_posts = user.sw_posts
    hw_posts = user.hw_posts
    return render_template('user.html', user=user, users=users, spell_posts=spell_posts, company_posts=company_posts, crops_posts=crops_posts, sw_posts=sw_posts, hw_posts=hw_posts)

@app.route('/success/<name>')
def success(name):
    return 'you got it %s' % name

@home_bp.route('/edit-user', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('home_bp.edit_user'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_user.html', title='Edit Profile', form=form)



@home_bp.route('/')
def home():
    if current_user.is_authenticated:
        flash('Welcome!', current_user)
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

@home_bp.route('/swcategories')
def swcategories():
    sw_categories_list = SWCategories.query.all()
    return render_template("sw_categories.html", sw_categories_list=sw_categories_list)

@home_bp.route('/hwcategories')
def hwcategories():
    hw_categories_list = HWCategories.query.all()
    return render_template("hw_categories.html", hw_categories_list=hw_categories_list)

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
    if g.user.is_authenticated:
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
    return redirect(url_for('home_bp.home'))

@home_bp.route('/add-new-history')
def add_new_history():
    if g.user.is_authenticated:
        form = HistoryForm()
        message=" "
        if form.validate_on_submit():
            return redirect(url_for("history-entry"))
        return render_template(
            "add_new_history.html",
            form=form,
            template="form-template",
            message=message
            )
    return redirect(url_for('home_bp.home'))

@home_bp.route('/add-new-location')
def add_new_location():
    if g.user.is_authenticated:
        form = LocationForm()
        message=" "
        if form.validate_on_submit():
            return redirect(url_for("location-entry"))
        return render_template(
            "add_new_location.html",
            form=form,
            template="form-template",
            message=message
            )
    return redirect(url_for('home_bp.home'))

@home_bp.route('/add-new-sw-category')
def add_new_sw_category():
    if g.user.is_authenticated:
        form = SWCategoryForm()
        message=" "
        if form.validate_on_submit():
            return redirect(url_for("sw-category-entry"))
        return render_template(
            "add_new_sw_category.html",
            form=form,
            template="form-template",
            message=message
            )
    return redirect(url_for('home_bp.home'))

@home_bp.route('/add-new-hw-category')
def add_new_hw_category():
    if g.user.is_authenticated:
        form = HWCategoryForm()
        message=" "
        if form.validate_on_submit():
            return redirect(url_for("hw-category-entry"))
        return render_template(
            "add_new_hw_category.html",
            form=form,
            template="form-template",
            message=message
            )
    return redirect(url_for('home_bp.home'))

@home_bp.route('/sw-category-entry', methods=['GET', 'POST'])
def sw_category_entry():
    form = SWCategoryForm()
    # POST: 
    if request.method == 'POST':
        if form.is_submitted():
            print ("submitted")
        if form.validate():
            print ("valid")
            print(form.errors)
        if form.validate_on_submit():
            # Get Form Field
            sw_categories_name = request.form['sw_categories_name']

            sw_categories = SWCategories(
                sw_categories_name=sw_categories_name
            )

            db.session.add(sw_categories)
            db.session.commit()
            flash('Record was successfully added')
            return render_template(
                'sw_category_entry.html',
                sw_categories=sw_categories
                )
        else:
            print("bad")
    return render_template('add_new_sw_category.html', form=form)

@home_bp.route('/hw-category-entry', methods=['GET', 'POST'])
def hw_category_entry():
    form = HWCategoryForm()
    # POST: 
    if request.method == 'POST':
        if form.is_submitted():
            print ("submitted")
        if form.validate():
            print ("valid")
            print(form.errors)
        if form.validate_on_submit():
            # Get Form Field
            hw_categories_name = request.form['hw_categories_name']

            hw_categories = HWCategories(
                hw_categories_name=hw_categories_name
            )

            db.session.add(hw_categories)
            db.session.commit()
            flash('Record was successfully added')
            return render_template(
                'hw_category_entry.html',
                hw_categories=hw_categories
                )
        else:
            print("bad")
    return render_template('add_new_hw_category.html', form=form)

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
            sw_categories = form.sw_categories.data
            sw_product_description = request.form['sw_product_description']
            sw_product_img = request.files['sw_product_img']
            sw_os_license = request.form['sw_os_license']
            sw_references = request.form['sw_references']
            sw_locations_desc = form.sw_locations_desc.data
            sw_locations_img = request.files['sw_locations_img']
            hw_id = form.hw_id.data
            companies_list = form.companies_list.data
            crops_id = form.crops_id.data
            user_id = current_user.get_id()

            print (sw_categories)
            if 'sw_product_img' not in request.files:
                flash('No hw_product_img part')
            
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

            sw_products = SWProducts(
                sw_company_name=sw_company_name, 
                sw_company_product=sw_company_product, 
                sw_software_components = sw_software_components,
                sw_product_description=sw_product_description, 
                sw_product_img=filename,
                sw_os_license=sw_os_license,
                sw_references=sw_references,
                sw_locations_desc = sw_locations_desc,
                sw_locations_img = sw_l_filename,
                user_id=user_id
                )

            db.session.add(sw_products)
            db.session.flush()

            software_id=sw_products.id

            hardwares = [i.id for i in hw_id]
            crops = [i.id for i in crops_id]
            companies = [i.id for i in companies_list]
            categories = [i.id for i in sw_categories]

            for hw in hardwares: 
                db.session.execute(software_hardware.insert().values([(software_id, hw)]))
            for c in crops: 
                db.session.execute(crops_software.insert().values([(c, software_id)]))
            for company in companies: 
                db.session.execute(companies_software.insert().values([(company, software_id)]))
            for cat in categories: 
                db.session.execute(software_sw_categories.insert().values([(software_id, cat)]))
            
            db.session.commit()
            flash('Record was successfully added')

            sh=db.session.query(software_hardware).all()
            cs=db.session.query(crops_software).all()
            compso=db.session.query(companies_software).all()
            softcat=db.session.query(software_sw_categories).all()

            hw_ids=[]
            crops_ids=[]
            companies_ids=[]
            categories_ids=[]

            for s in sh:   
                if s.software_id is not None:
                    query_hard = HWProducts.query.filter_by(id = s.hardware_id).all()
                    query_soft = SWProducts.query.filter_by(id = s.software_id).all()

                    for softwares in query_soft:
                        if softwares.id == sw_products.id:
                            for hardwares in query_hard:
                                hw_ids.append(hardwares.id) 

            for s in cs:   
                if s.software_id is not None:
                    query_soft = SWProducts.query.filter_by(id = s.software_id).all()
                    query_crop = Crops.query.filter_by(id = s.crops_id).all()

                    for softwares in query_soft:
                        if softwares.id == sw_products.id:
                            for crops in query_crop:
                                crops_ids.append(crops.id) 
                                
            for s in compso:   
                if s.software_id is not None:
                    query_soft = SWProducts.query.filter_by(id = s.software_id).all()
                    query_company = Companies.query.filter_by(id = s.companies_id).all()

                    for softwares in query_soft:
                        if softwares.id == sw_products.id:
                            for companies in query_company:
                                companies_ids.append(companies.id)

            for cat in softcat:   
                if cat.software_id is not None:
                    query_soft = SWProducts.query.filter_by(id = cat.software_id).all()
                    query_category = SWCategories.query.filter_by(id = cat.sw_categories_id).all()

                    for softwares in query_soft:
                        if softwares.sw_company_product == sw_products.sw_company_product:
                            for category in query_category:
                                categories_ids.append(category.id)
                                print(category.sw_categories_name)  

            hw_list = HWProducts.query.filter(HWProducts.id.in_(hw_ids)).all()
            crops_list = Crops.query.filter(Crops.id.in_(crops_ids)).all()
            companies_list = Companies.query.filter(Companies.id.in_(companies_ids)).all()
            categories_list = SWCategories.query.filter(SWCategories.id.in_(categories_ids)).all()

            hw_ids=[]
            crops_ids=[]
            companies_ids=[]
            categories_ids=[]
            
            return render_template(
                'software_entry.html',
                sw_products=sw_products,
                hw_list=hw_list,
                crops_list=crops_list,
                companies_list=companies_list,
                categories_list=categories_list
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
            # print ("valid")
            print(form.errors)
        if form.validate_on_submit():
            # Get Form Fields
            hw_company_name = request.form['hw_company_name']
            hw_company_product = request.form['hw_company_product']
            hw_hardware_components = request.form['hw_hardware_components']
            hw_categories = form.hw_categories.data
            sw_id = form.sw_id.data
            companies_list = form.companies_list.data
            hw_product_description = request.form['hw_product_description']
            hw_product_img = request.files['hw_product_img']
            hw_references = request.form['hw_references']
            hw_locations_desc = form.hw_locations_desc.data
            hw_locations_img = request.files['hw_locations_img']
            crops_id = form.crops_id.data
            user_id = current_user.get_id()
            
            if 'hw_product_img' not in request.files:
                flash('No hw_product_img part')

            if hw_product_img:
                filename = secure_filename(hw_product_img.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                hw_product_img.save(os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename))

            if hw_locations_img:
                hw_l_filename = secure_filename(hw_locations_img.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                hw_locations_img.save(os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], hw_l_filename))
       
            hw_products = HWProducts(
                hw_company_name=hw_company_name, 
                hw_company_product=hw_company_product, 
                hw_hardware_components = hw_hardware_components,
                hw_product_description=hw_product_description, 
                hw_product_img=filename,
                hw_references=hw_references,
                hw_locations_desc = hw_locations_desc,
                hw_locations_img = hw_l_filename,
                user_id=user_id
                )

            db.session.add(hw_products)
            db.session.flush()

            hardware_id=hw_products.id

            softwares = [i.id for i in sw_id]
            print(softwares)
            crops = [i.id for i in crops_id]
            companies = [i.id for i in companies_list]
            categories = [i.id for i in hw_categories]

            for sw in softwares: 
                db.session.execute(software_hardware.insert().values([(sw, hardware_id)]))
            for c in crops: 
                db.session.execute(crops_hardware.insert().values([(c, hardware_id)]))
            for company in companies: 
                db.session.execute(companies_hardware.insert().values([(company, hardware_id)]))
            for cat in categories: 
                db.session.execute(hardware_hw_categories.insert().values([(hardware_id, cat)]))
            
            db.session.commit()

            hs=db.session.query(software_hardware).all()
            ch=db.session.query(crops_hardware).all()
            compha=db.session.query(companies_hardware).all()
            hardcat=db.session.query(hardware_hw_categories).all()

            sw_ids=[]
            crops_ids=[]
            companies_ids=[]
            categories_ids=[]

            for h in hs:   
                if h.hardware_id is not None:
                    query_hard = HWProducts.query.filter_by(id = h.hardware_id).all()
                    query_soft = SWProducts.query.filter_by(id = h.software_id).all()

                    for hardwares in query_hard:
                        if hardwares.hw_company_product == hw_products.hw_company_product:
                            for softwares in query_soft:
                                sw_ids.append(softwares.id) 
            for h in ch:   
                if h.hardware_id is not None:
                    query_hard = HWProducts.query.filter_by(id = h.hardware_id).all()
                    query_crop = Crops.query.filter_by(id = h.crops_id).all()

                    for hardwares in query_hard:
                        if hardwares.hw_company_product == hw_products.hw_company_product:
                            for crops in query_crop:
                                crops_ids.append(crops.id) 
                                print(crops.crop_name)
            for h in compha:   
                if h.hardware_id is not None:
                    query_hard = HWProducts.query.filter_by(id = h.hardware_id).all()
                    query_company = Companies.query.filter_by(id = h.companies_id).all()

                    for hardwares in query_hard:
                        if hardwares.hw_company_product == hw_products.hw_company_product:
                            for companies in query_company:
                                companies_ids.append(companies.id)
                                print(companies.company_name)
            for cat in hardcat:   
                if cat.hardware_id is not None:
                    query_hard = HWProducts.query.filter_by(id = cat.hardware_id).all()
                    query_category = HWCategories.query.filter_by(id = cat.hw_categories_id).all()

                    for hardwares in query_hard:
                        if hardwares.hw_company_product == hw_products.hw_company_product:
                            for category in query_category:
                                categories_ids.append(category.id)
                                print(category.hw_categories_name)


            sw_list = SWProducts.query.filter(SWProducts.id.in_(sw_ids)).all()
            crops_list = Crops.query.filter(Crops.id.in_(crops_ids)).all()
            companies_list = Companies.query.filter(Companies.id.in_(companies_ids)).all()
            categories_list = HWCategories.query.filter(HWCategories.id.in_(categories_ids)).all()

            sw_ids=[]
            crops_ids=[]
            companies_ids=[]
            categories_ids=[]
            print(crops_ids)

            return render_template(
                'hardware_entry.html',
                hw_products=hw_products,
                sw_list=sw_list,
                crops_list=crops_list,
                companies_list=companies_list,
                categories_list=categories_list
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
            print ("valid")
        if form.validate():
            print ("valid")
        print(form.errors)
        if form.validate_on_submit():
            # Get Form Fields
            crop_name = request.form['crop_name']
            genus_species = request.form['genus_species']
            crop_intellectual_property = request.form['crop_intellectual_property']
            crop_chemicals_used = request.form['crop_chemicals_used']
            sw_id = form.sw_id.data
            hw_id = form.hw_id.data
            companies_list = form.companies_list.data
            crop_genetic_information = request.form['crop_genetic_information']
            crop_companions = request.form['crop_companions']
            crop_description = request.form['crop_description']
            crop_img = request.files['crop_img']
            crop_references = request.form['crop_references']
            crop_locations = form.crop_locations.data
            user_id = current_user.get_id()
            
            if 'crop_img' not in request.files:
                flash('No crop image')

            if crop_img:
                filename = secure_filename(crop_img.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                crop_img.save(os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename))

            crops = Crops(
                crop_name=crop_name, 
                genus_species=genus_species, 
                crop_intellectual_property = crop_intellectual_property,
                crop_chemicals_used = crop_chemicals_used,
                crop_genetic_information = crop_genetic_information,
                crop_companions=crop_companions, 
                crop_description=crop_description,
                crop_img=filename,
                crop_references=crop_references,
                crop_locations = crop_locations,
                user_id=user_id
                )

            db.session.add(crops)

            db.session.flush()

            crops_id=crops.id

            softwares = [i.id for i in sw_id]
            hardwares = [i.id for i in hw_id]
            companies = [i.id for i in companies_list]

            for s in softwares: 
                db.session.execute(crops_software.insert().values([(crops_id, s)]))
            for hw in hardwares: 
                db.session.execute(crops_hardware.insert().values([(crops_id, hw)]))
            for company in companies: 
                db.session.execute(crops_companies.insert().values([(crops_id, company)]))

            
            db.session.commit()
            flash('Record was successfully added')

            cs=db.session.query(crops_software).all()
            ch=db.session.query(crops_hardware).all()
            croco=db.session.query(crops_companies).all()

            hw_ids=[]
            sw_ids=[]
            companies_ids=[]

            for c in cs:   
                if c.crops_id is not None:
                    query_crop = Crops.query.filter_by(id = c.crops_id).all()
                    query_soft = SWProducts.query.filter_by(id = c.software_id).all()

                    for crop in query_crop:
                        if crop.id == crops.id:
                            for softwares in query_soft:
                                sw_ids.append(softwares.id) 

            for c in ch:   
                if c.crops_id is not None:
                    query_hard = HWProducts.query.filter_by(id = c.hardware_id).all()
                    query_crop = Crops.query.filter_by(id = c.crops_id).all()

                    for crop in query_crop:
                        if crop.id == crops.id:
                            for hardwares in query_hard:
                                hw_ids.append(hardwares.id) 
                                
            for c in croco:   
                if c.crops_id is not None:
                    query_crop = Crops.query.filter_by(id = c.crops_id).all()
                    query_company = Companies.query.filter_by(id = c.companies_id).all()

                    for crop in query_crop:
                        if crop.id == crops.id:
                            for companies in query_company:
                                companies_ids.append(companies.id)
                                
            hw_list = HWProducts.query.filter(HWProducts.id.in_(hw_ids)).all()
            sw_list = SWProducts.query.filter(SWProducts.id.in_(sw_ids)).all()
            companies_list = Companies.query.filter(Companies.id.in_(companies_ids)).all()

            hw_ids=[]
            sw_ids=[]
            companies_ids=[]

            return render_template(
                'crop_entry.html',
                crops=crops,
                hw_list=hw_list,
                sw_list=sw_list,
                companies_list=companies_list
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
            company_name = request.form['company_name']
            company_keywords = request.form['company_keywords']
            company_board_members = request.form['company_board_members']
            sw_id = form.sw_id.data
            hw_id = form.hw_id.data
            company_description = request.form['company_description']
            company_img = request.files['company_img']
            crops_id = form.crops_id.data
            related_companies = request.form['related_companies']
            company_profits = request.form['company_profits']
            user_id = current_user.get_id()
            
            if 'company_img' not in request.files:
                flash('No company image')

            if company_img:
                filename = secure_filename(company_img.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                company_img.save(os.path.join(basedir, app.config['UPLOADED_IMAGES_DEST'], filename))

            companies = Companies(
                company_name = company_name,
                company_keywords = company_keywords,
                company_board_members = company_board_members,
                company_description = company_description,
                company_img=filename, 
                related_companies=related_companies,
                company_profits=company_profits,
                user_id=user_id
                )

            db.session.add(companies)

            db.session.flush()

            companies_id=companies.id

            softwares = [i.id for i in sw_id]
            hardwares = [i.id for i in hw_id]
            crops = [i.id for i in crops_id]

            for s in softwares: 
                db.session.execute(companies_software.insert().values([(companies_id, s)]))
            for hw in hardwares: 
                db.session.execute(companies_hardware.insert().values([(companies_id, hw)]))
            for c in crops: 
                db.session.execute(crops_companies.insert().values([(c, companies_id)]))

            
            db.session.commit()
            flash('Record was successfully added')

            cs=db.session.query(companies_software).all()
            ch=db.session.query(companies_hardware).all()
            croco=db.session.query(crops_companies).all()

            hw_ids=[]
            sw_ids=[]
            crops_ids=[]

            for c in cs:   
                if c.companies_id is not None:
                    query_company = Companies.query.filter_by(id = c.companies_id).all()
                    query_soft = SWProducts.query.filter_by(id = c.software_id).all()

                    for co in query_company:
                        if co.id == companies.id:
                            for softwares in query_soft:
                                sw_ids.append(softwares.id) 

            for c in ch:   
                if c.companies_id is not None:
                    query_hard = HWProducts.query.filter_by(id = c.hardware_id).all()
                    query_company = Companies.query.filter_by(id = c.companies_id).all()

                    for co in query_company:
                        if co.id == companies.id:
                            for hardwares in query_hard:
                                hw_ids.append(hardwares.id) 
                                
            for c in croco:   
                if c.companies_id is not None:
                    query_crop = Crops.query.filter_by(id = c.crops_id).all()
                    query_company = Companies.query.filter_by(id = c.companies_id).all()

                    for co in query_company:
                        if co.id == companies.id:
                            for crops in query_crop:
                                crops_ids.append(crops.id)
                                
            hw_list = HWProducts.query.filter(HWProducts.id.in_(hw_ids)).all()
            sw_list = SWProducts.query.filter(SWProducts.id.in_(sw_ids)).all()
            crops_list = Crops.query.filter(Crops.id.in_(crops_ids)).all()

            hw_ids=[]
            sw_ids=[]
            crops_ids=[]

            return render_template(
                'company_entry.html',
                companies=companies,
                hw_list=hw_list,
                sw_list=sw_list,
                crops_list=crops_list
                )
        else:
            print("bad")
    return render_template('add_new_crop.html', form=form)


@home_bp.route('/magickal-entry', methods=['GET', 'POST'])
def magickal_entry():
    if g.user.is_authenticated:
        flash('Welcome!', current_user)
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
            spell_locations = form.spell_locations.data
            spell_networks = request.form['spell_networks']
            spell_timestamp = datetime.utcnow()
            user_id = current_user.get_id()

            
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
                spell_networks=spell_networks,
                spell_timestamp=spell_timestamp,
                # user=user,
                user_id=user_id
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

#many to many test
@home_bp.route('/history-entry', methods=['GET', 'POST'])
def history_entry():
    if g.user.is_authenticated:
        flash('Welcome!', current_user)
        form = HistoryForm()
    # POST: 

    if request.method == 'POST':
        if form.is_submitted():
            print ("submitted")
        if form.validate():
            print ("valid")
            print(form.errors)
        if form.validate_on_submit():
            # Get Form Fields
            history_name = request.form['history_name']
            user_id = current_user.get_id()
            locations_list = form.locations_list.data

            history = History(
                history_name=history_name,
                user_id=user_id
                )
            db.session.add(history)
            db.session.flush()

            history_id = history.id
            
            db.session.commit()
            
            locations = [i.id for i in locations_list.query.all()]

            for l in locations: 
                if l==locations_list.id:
                    db.session.execute(history_locations.insert().values([(history_id, l)]))

            print(locations_list.id)
            
            db.session.commit()

            hl=db.session.query(history_locations).all()

            for h in hl:   
                if h.history_id is not None:
                    query_hists = History.query.filter_by(id = h.history_id).all()
                    query_locs = Locations.query.filter_by(id = h.locations_id).all()


                    for historee in query_hists:
                        if historee.history_name == history.history_name:
                            for loc in query_locs:
                                print(loc.location_name )

            flash('Record was successfully added')

            return render_template(
                'history_entry.html',
                history=history,
                history_id=history_id
                )
        else:
            print("bad")
    return render_template('add_new_history.html', form=form)

#many to many test
@home_bp.route('/location-entry', methods=['GET', 'POST'])
def location_entry():
    if g.user.is_authenticated:
        flash('Welcome!', current_user)
        form = LocationForm()
    # POST: 

    if request.method == 'POST':
        if form.is_submitted():
            print ("submitted")
        if form.validate():
            print ("valid")
        print(form.errors)
        if form.validate_on_submit():
               # Get Form Fields
            location_name = request.form['location_name']
            history_list = form.history_list.data
            user_id = current_user.get_id()
            #  a = Author(firstname= form.firstname.data, familyname= form.familyname.data)
            # a.booksd = form.book_list.data

            #query that matches name to id
            if history_list is not None:
                history_list = Locations.query.filter(History.id.in_(form.history_list.data)).all()

                for h in history_list:
                    locations.hist_of_place.append(h)

            locations = Locations(
                location_name=location_name,
                user_id=user_id
                )

            db.session.add(locations)
            db.session.commit()
            flash('Record was successfully added')

            return render_template(
                'location_entry.html',
                locations=locations
                )
        else:
            print("bad")
    return render_template('add_new_location.html', form=form)

@home_bp.route('/swcategory/<int:id>')
def show_sw_category_entry(id):
    sw_categories = SWCategories.query.filter_by(id=id).first_or_404()

    return render_template(
        'sw_category_entry.html', 
        sw_categories=sw_categories
        )

@home_bp.route('/hwcategory/<int:id>')
def show_hw_category_entry(id):
    hw_categories = HWCategories.query.filter_by(id=id).first_or_404()

    return render_template(
        'hw_category_entry.html', 
        hw_categories=hw_categories
        )

@home_bp.route('/software/<int:id>')
def show_sw_entry(id):
    sw_products = SWProducts.query.filter_by(id=id).first_or_404()

    sh=db.session.query(software_hardware).all()
    cs=db.session.query(crops_software).all()
    compso=db.session.query(companies_software).all()
    softcat=db.session.query(software_sw_categories).all()

    hw_ids=[]
    crops_ids=[]
    companies_ids=[]
    categories_ids=[]

    for s in sh:   
        if s.software_id is not None:
            query_hard = HWProducts.query.filter_by(id = s.hardware_id).all()
            query_soft = SWProducts.query.filter_by(id = s.software_id).all()

            for softwares in query_soft:
                if softwares.id == sw_products.id:
                    for hardwares in query_hard:
                        hw_ids.append(hardwares.id) 

    for s in cs:   
        if s.software_id is not None:
            query_soft = SWProducts.query.filter_by(id = s.software_id).all()
            query_crop = Crops.query.filter_by(id = s.crops_id).all()

            for softwares in query_soft:
                if softwares.id == sw_products.id:
                    for crops in query_crop:
                        crops_ids.append(crops.id) 
                        
    for s in compso:   
        if s.software_id is not None:
            query_soft = SWProducts.query.filter_by(id = s.software_id).all()
            query_company = Companies.query.filter_by(id = s.companies_id).all()

            for softwares in query_soft:
                if softwares.id == sw_products.id:
                    for companies in query_company:
                        companies_ids.append(companies.id)
    for cat in softcat:   
        if cat.software_id is not None:
            query_soft = SWProducts.query.filter_by(id = cat.software).all()
            query_category = SWCategories.query.filter_by(id = cat.sw_categories_id).all()

            for softwares in query_soft:
                if softwares.sw_company_product == sw_products.sw_company_product:
                    for category in query_category:
                        categories_ids.append(category.id)
                        print(category.sw_categories_name)

    hw_list = HWProducts.query.filter(HWProducts.id.in_(hw_ids)).all()
    crops_list = Crops.query.filter(Crops.id.in_(crops_ids)).all()
    companies_list = Companies.query.filter(Companies.id.in_(companies_ids)).all()
    categories_list = SWCategories.query.filter(SWCategories.id.in_(categories_ids)).all()

    hw_ids=[]
    crops_ids=[]
    companies_ids=[]
    categories_ids=[]

    return render_template(
        'software_entry.html', 
        sw_products=sw_products,
        hw_list=hw_list,
        crops_list=crops_list,
        companies_list=companies_list,
        categories_list=categories_list
        )

@home_bp.route('/hardware/<int:id>')
def show_hw_entry(id):
    hw_products = HWProducts.query.filter_by(id=id).first_or_404()

    hs=db.session.query(software_hardware).all()
    ch=db.session.query(crops_hardware).all()
    compha=db.session.query(companies_hardware).all()
    hardcat=db.session.query(hardware_hw_categories).all()

    sw_ids=[]
    crops_ids=[]
    companies_ids=[]
    categories_ids=[]

    for h in hs:   
        if h.hardware_id is not None:
            query_hard = HWProducts.query.filter_by(id = h.hardware_id).all()
            query_soft = SWProducts.query.filter_by(id = h.software_id).all()

            for hardwares in query_hard:
                if hardwares.id == hw_products.id:
                    for softwares in query_soft:
                        sw_ids.append(softwares.id) 
                        # print(softwares.sw_company_product )
    for h in ch:   
        if h.hardware_id is not None:
            query_hard = HWProducts.query.filter_by(id = h.hardware_id).all()
            query_crop = Crops.query.filter_by(id = h.crops_id).all()


            for hardwares in query_hard:
                if hardwares.id == hw_products.id:
                    for crops in query_crop:
                        crops_ids.append(crops.id) 
                        print(crops.crop_name)
    for h in compha:   
        if h.hardware_id is not None:
            query_hard = HWProducts.query.filter_by(id = h.hardware_id).all()
            query_company = Companies.query.filter_by(id = h.companies_id).all()


            for hardwares in query_hard:
                if hardwares.hw_company_product == hw_products.hw_company_product:
                    for companies in query_company:
                        companies_ids.append(companies.id)
                        print(companies.company_name)
    for cat in hardcat:   
                if cat.hardware_id is not None:
                    query_hard = HWProducts.query.filter_by(id = cat.hardware_id).all()
                    query_category = HWCategories.query.filter_by(id = cat.hw_categories_id).all()

                    for hardwares in query_hard:
                        if hardwares.hw_company_product == hw_products.hw_company_product:
                            for category in query_category:
                                categories_ids.append(category.id)
                                print(category.hw_categories_name)

    sw_list = SWProducts.query.filter(SWProducts.id.in_(sw_ids)).all()
    crops_list = Crops.query.filter(Crops.id.in_(crops_ids)).all()
    companies_list = Companies.query.filter(Companies.id.in_(companies_ids)).all()
    categories_list = HWCategories.query.filter(HWCategories.id.in_(categories_ids)).all()

    sw_ids=[]
    crops_ids=[]
    companies_ids=[]
    categories_ids=[]

    return render_template(
        'hardware_entry.html', 
        hw_products=hw_products,
        sw_list=sw_list,
        crops_list=crops_list,
        companies_list=companies_list,
        categories_list=categories_list
        )

@home_bp.route('/crops/<int:id>')
def show_crop_entry(id):
    crops = Crops.query.filter_by(id=id).first_or_404()

    cs=db.session.query(crops_software).all()
    ch=db.session.query(crops_hardware).all()
    croco=db.session.query(crops_companies).all()

    hw_ids=[]
    sw_ids=[]
    companies_ids=[]

    for c in cs:   
        if c.crops_id is not None:
            query_crop = Crops.query.filter_by(id = c.crops_id).all()
            query_soft = SWProducts.query.filter_by(id = c.software_id).all()

            for crop in query_crop:
                if crop.id == crops.id:
                    for softwares in query_soft:
                        sw_ids.append(softwares.id) 

    for c in ch:   
        if c.crops_id is not None:
            query_hard = HWProducts.query.filter_by(id = c.hardware_id).all()
            query_crop = Crops.query.filter_by(id = c.crops_id).all()

            for crop in query_crop:
                if crop.id == crops.id:
                    for hardwares in query_hard:
                        hw_ids.append(hardwares.id) 
                        
    for c in croco:   
        if c.crops_id is not None:
            query_crop = Crops.query.filter_by(id = c.crops_id).all()
            query_company = Companies.query.filter_by(id = c.companies_id).all()

            for crop in query_crop:
                if crop.id == crops.id:
                    for companies in query_company:
                        companies_ids.append(companies.id)
                        
    hw_list = HWProducts.query.filter(HWProducts.id.in_(hw_ids)).all()
    sw_list = SWProducts.query.filter(SWProducts.id.in_(sw_ids)).all()
    companies_list = Companies.query.filter(Companies.id.in_(companies_ids)).all()

    hw_ids=[]
    sw_ids=[]
    companies_ids=[]

    return render_template(
        'crop_entry.html', 
        crops=crops,
        hw_list=hw_list,
        sw_list=sw_list,
        companies_list=companies_list
        )

@home_bp.route('/companies/<int:id>')
def show_company_entry(id):
    companies = Companies.query.filter_by(id=id).first_or_404()

    cs=db.session.query(companies_software).all()
    ch=db.session.query(companies_hardware).all()
    croco=db.session.query(crops_companies).all()

    hw_ids=[]
    sw_ids=[]
    crops_ids=[]

    for c in cs:   
        if c.companies_id is not None:
            query_company = Companies.query.filter_by(id = c.companies_id).all()
            query_soft = SWProducts.query.filter_by(id = c.software_id).all()

            for co in query_company:
                if co.id == companies.id:
                    for softwares in query_soft:
                        sw_ids.append(softwares.id) 

    for c in ch:   
        if c.companies_id is not None:
            query_hard = HWProducts.query.filter_by(id = c.hardware_id).all()
            query_company = Companies.query.filter_by(id = c.companies_id).all()

            for co in query_company:
                if co.id == companies.id:
                    for hardwares in query_hard:
                        hw_ids.append(hardwares.id) 
                        
    for c in croco:   
        if c.companies_id is not None:
            query_crop = Crops.query.filter_by(id = c.crops_id).all()
            query_company = Companies.query.filter_by(id = c.companies_id).all()

            for co in query_company:
                if co.id == companies.id:
                    for crops in query_crop:
                        crops_ids.append(crops.id)
                        
    hw_list = HWProducts.query.filter(HWProducts.id.in_(hw_ids)).all()
    sw_list = SWProducts.query.filter(SWProducts.id.in_(sw_ids)).all()
    crops_list = Crops.query.filter(Crops.id.in_(crops_ids)).all()

    hw_ids=[]
    sw_ids=[]
    crops_ids=[]

    return render_template(
        'company_entry.html', 
        companies=companies,
        hw_list=hw_list,
        sw_list=sw_list,
        crops_list=crops_list
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


@home_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500