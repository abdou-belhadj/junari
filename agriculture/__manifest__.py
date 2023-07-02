# -*- coding: utf-8 -*-
{
    'name': "agriculture",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Abdou Belhadj",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Agriculture',
    'version': '16.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/res_farmers_view.xml',
        'views/crops_crops_view.xml',
        'views/crops_configuration.xml',
        'views/disease_view.xml',
        'views/process_process_view.xml',
        'views/crops_process_view.xml',
        'views/product_views.xml',
        'views/menus.xml',
    ],
}
