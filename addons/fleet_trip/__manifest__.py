{
    'name': 'Fleet Trip',
    'summary': 'Fleet Trip',
    'description': 'Fleet Trip',
    'category': 'fleet',
    'version': '14.0.1.0.0',
    'depends': ['product', 'contacts', 'hr', 'maintenance', 'web_backend', 'rest_api', 'ir_attachment_url',
                'vn_address', 'stock', 'fleet'],
    'data': [
        'data/location_data.xml',
        'security/fleet_security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/fleet_info_view.xml',
        'views/fleet_product_view.xml',
        'views/fleet_job_rank_view.xml',
        'wizard/fleet_trip_approve_reject_view.xml',
        'views/fleet_trip_view.xml',
        # 'views/fleet_car_view.xml',
        'views/maintenance_equipment_view.xml',
        'views/product_view.xml',
        'views/stock_delivery_view.xml',
        'wizard/fleet_trip.xml',
        'wizard/fleet_trip_cost_generate_view.xml',
        'report/fleet_main_report_view.xml',
        'data/product_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'fleet_trip/static/src/css/custom_styles.css'
        ]
    },
    'application': True,
    'installable': True,
}
