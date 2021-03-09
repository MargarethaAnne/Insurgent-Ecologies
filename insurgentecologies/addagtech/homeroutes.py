# pylint: disable=no-member
from flask import current_app as app
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint, make_response
import json
import os.path
from werkzeug.utils import secure_filename

from .forms import CompanyProductForm

from datetime import datetime as dt
from .models import CompanyProducts, db

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/')
def home():
    return render_template('home.html')
    # return render_template('index.html', codes=session.keys())

@home_bp.route('/categories')
def categories():
    return render_template('categories-page.html')

@home_bp.route('/subcategories')
def subcategories():
   return render_template("list.html")
   
@home_bp.route('/add-new-agtech')
def add_new():
    form = CompanyProductForm()
    if form.validate_on_submit():
        return redirect(url_for("ag-tech-entry"))
    return render_template(
        "add_new_agtech.html",
        form=form,
        template="form-template"
    )

@home_bp.route('/ag-tech-entry', methods=['GET', 'POST'])
def ag_tech_entry():
    form = CompanyProductForm(request.form)
    # POST: 
    if request.method == 'POST':
        if form.validate():
            # Get Form Fields
            company_name = request.form.get('company_name')
            company_product = request.form.get('company_product')
            img_url = request.form.get('img_url')

            existing_product = CompanyProducts.query.filter_by(company_product=company_product).first()
            if existing_product:
                return make_response(f"{company_name} ({company_product}) already created!")
            if existing_product is None:
                company_products = CompanyProductForm(
                    company_name=company_name,
                    company_product=company_product,
                    img_url = img_url
                )
            db.session.add(company_products)
            db.session.commit()
            flash('Record was successfully added')
            redirect(url_for('add_new_agtech.html'))
    # GET: Serve Sign-up page
    return render_template(
        'ag_tech_entry.html',
        title='Create an Account | Flask-Login Tutorial.',
        form=form,
        template='form-template',
    )
   


    # if request.method == 'POST':
    #     company_names = {}

    #     if os.path.exists('company_names.json'):
    #         with open('company_names.json') as company_names_file:
    #             company_names=json.load(company_names_file)

    #     if request.form['company_product'] in company_names.keys():
    #         flash('already taken')
    #         return redirect(url_for('addagtech.add_new'))

    #     if 'company_name' in request.form.keys():
    #         # company_names[request.form['company_product']] = {'company_name': request.form['company_name']}
    #         f = request.files['file']
    #         full_name = secure_filename(f.filename)
    #         f.save('/Users/margarethahaughwout/Documents/projects/cointelpro-desktop/insurgentecologies/addagtech/static/user_files/' + full_name)
    #         company_names[request.form['company_product']] = {'company_product': request.form['company_product'], 'company_name': request.form['company_name'], 'file': full_name}

    #     with open('company_names.json', 'w') as company_name_file:
    #         json.dump(company_names, company_name_file)
    #         session[request.form['company_product']] = True
    #     return render_template('ag_tech_entry.html', company_product=request.form['company_product'], company_name=request.form['company_name'], img_url=full_name)
    # else:
    #     return redirect(url_for('addagtech.add_new'))

@home_bp.route('/add-new-agtech/<string:company_product>')
def display(company_product): 
    if os.path.exists('company_names.json'):
        with open('company_names.json') as company_names_file:
            company_names = json.load(company_names_file)
            if company_product in company_names.keys():
                if 'company_name' in company_names[company_product].keys():
                    return company_names[company_product]['company_name'], company_names[company_product]['company_name']['file']
                    # return redirect(company_names[company_product]['company_name'], company_names[company_product]['file'])
                # else:
                #     return redirect(url_for('static', filename='user_files/' + company_names[company_product]['file']))
    return abort(404)

@home_bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@home_bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))