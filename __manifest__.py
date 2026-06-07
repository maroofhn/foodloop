{
    'name': 'FoodLoop',
    'summary': 'Surplus food rescue and redistribution tracker',
    'version': '19.0.1.0.0',
    'category': 'Other',
    'author': 'FoodLoop Team',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts', 'product', 'mail'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'data/foodloop_sequence.xml',
        'views/food_surplus_listing_views.xml',
        'views/foodloop_menus.xml',
        'data/foodloop_demo.xml',
    ],
}
