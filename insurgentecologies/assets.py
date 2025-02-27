"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    """Create stylesheet bundles."""
    assets.auto_build = True
    assets.debug = False
    # common_less_bundle = Bundle(
    #     'tech/style.css',
    #     filters='cssmin',
    #     output='dist/css/style.css',
    #     extra={'rel': 'stylesheet/less'}
    # )
    home_css_bundle = Bundle(
        'home_bp/tech/categories-menu.css',
        'home_bp/tech/menu.css',
        'home_bp/tech/homestyle.css',
        'home_bp/tech/entry.css',
        'home_bp/tech/style.css',
        filters='cssmin',
        output='dist/css/home.css',
        extra={'rel': 'stylesheet/css'}
    )
    # profile_less_bundle = Bundle(
    #     'profile_bp/less/profile.less',
    #     filters='less,cssmin',
    #     output='dist/css/profile.css',
    #     extra={'rel': 'stylesheet/less'}
    # )
    # product_less_bundle = Bundle(
    #     'products_bp/less/products.less',
    #     filters='less,cssmin',
    #     output='dist/css/products.css',
    #     extra={'rel': 'stylesheet/less'}
    # )
    # assets.register('common_less_bundle', common_less_bundle)
    assets.register('home_css_bundle', home_css_bundle)
    # assets.register('profile_less_bundle', profile_less_bundle)
    # assets.register('product_less_bundle', product_less_bundle)
    if app.config['FLASK_ENV'] == 'development':
        # common_less_bundle.build()
        home_css_bundle.build()
        # profile_less_bundle.build()
        # product_less_bundle.build()
    return assets