# -*- coding: utf-8 -*-
{
    'name': "agriculture",

    'summary': """
        Comprehensive solution designed to streamline and manage agricultural operations.""",

    'description': """
        It caters to the specific needs of the agriculture industry, providing tools and functionalities 
         to optimize farm management, crop cultivation, inventory control, resource allocation, and reporting..
    """,

    'author': "Abdou Belhadj",

    'category': 'Agriculture',
    'version': '16.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_farmers_view.xml',
        'views/crops_crops_view.xml',
        'views/crops_stages.xml',
        'views/disease_view.xml',
        'views/process_view.xml',
        'views/crops_process_view.xml',
        'views/product_views.xml',
        'wizard/crops_stock_view.xml',
        'views/menus.xml',
        'data/data.xml',
        'data/crops_stages.xml',
        'data/crops_process.xml',
        'data/crops_diseases.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,

}
