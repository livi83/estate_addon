{
    'name': 'Estate',
    'version': '1.0',
    'category':'Real Estate/Brokerage',
    'summary': 'An estate modul',
    'description': 'Description',
    'author': 'Lívia Kelebercová',
    'depends': ['base','account'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_property_views.xml',
        'views/estate_property_search.xml',
        'views/estate_property_actions.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_actions.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_res_users_views.xml',
        'views/estate_menus.xml',
        
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/src/css/style.css',
        ],
        #'web.assets_frontend': [
         #   'static/src/css/style.css',
        #],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
