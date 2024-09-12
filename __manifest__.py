{
    'name': 'Estate',
    'version': '1.0',
    'category':'Real Estate/Brokerage',
    'summary': 'An estate modul',
    'description': 'Description',
    'author': 'Lívia Kelebercová',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
