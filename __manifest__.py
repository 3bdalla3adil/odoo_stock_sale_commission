# -*- coding: utf-8 -*-
{
    'name': "Stock Sales Commissioner",

    'summary': "An odoo module that calculate stock, sales commission based on companies commission",

    'description': """
     Assuming that each product purchased then marked as consignment  """,
    'author': "Eng. Abdulla Bashir",
    'website': "https://www.3bdalla3adil.github.io",
    'category': 'Sales',
    'version': '0.1',

    'depends': ['base','stock','sale','purchase','contacts','account'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

