# -*- coding: utf-8 -*-
from .main import *
import datetime

OUT_SUCCESS_CODE = 200
OUT_address_schema = (
    "id",
    "name",
)

OUT_fleet_location_schema = (
    "id",
    "name",
    ("ward_id", ("id", "name")),
    ("district_id", ("id", "name")),
    ("state_id", ("id", "name")),
)

OUT_FLEET_TRIP_schema = (
    "id",
    ("equipment_id", (
        "id",
        "name",
        "license_plate",
    ),),
    # ("location_id", (
    #     "id",
    #     "name"
    # ),),
    # ("location_dest_id", (
    #     "id",
    #     "name"
    # ),),
    "location_name",
    "location_dest_name",
    "incurred_fee",
    "incurred_note",
    "incurred_fee_2",
    "incurred_note_2",
    "schedule_date",
    "start_date",
    "end_date",
    "state",
    "ward_id",
    "district_id",
    "state_id",
    "ward_dest_id",
    "district_dest_id",
    "state_dest_id",
    "company_name",
    "eating_fee",
    "law_money",
    "road_tiket_fee",
    "fee_total",
    "odometer_start",
    "odometer_dest",
    ("attachment_ids", [(
        "url",
    )]),
)

OUT_model_res_user_read_one_SCHEMA = (
    "id",
    "name",
    ("equipment_ids", [("id", "name", "license_plate", "trip_count", "last_request")]),
    ("employee_id", (
        "id",
        "mobile_phone",
        "trip_count",
        "trip_done_count",
        "other_info",
        "salary_last_month",
        "contract_date",
        ("payroll_ids", [("id", "name", "total_amount")]),
        "payroll_total_amount",
        "job_title",
        ("department_id", (
            "id",
            "name"
        ),),
        ("parent_id", (
            "id",
            "name"
        ),),
        "identification_id",
        "gender",
        "birthday",
        ("address_home_id", (
            "street",
            "street2",
            "city",
            ("state_id",
             (
                 "id",
                 "name"
             ),),
            "phone",
            "mobile",
        ),
         ),
        ("message_ids", [(
            "date",
            "body",
            ("author_id", (
                "id",
                "name"
            )),
        )]),
    ),
     ))

OUT_maintenance_equipment_schema = (
    "id",
    "name",
    ("owner_user_id", ("id", "name")),
    "last_request",
    "license_plate",
    "trip_count",
    "note",
    ("message_ids", [(
        "date",
        "body",
        ("author_id", (
            "id",
            "name"
        )),
    )]),
)

OUT_maintenance_request_schema = (
    "id",
    "name",
    ("equipment_id", (
        "id",
        "name",
        "license_plate",
    )),
    "request_date",
    ("user_id", (
        "id",
        "name"
    )),
    ("create_uid", (
        "id",
        "name"
    )),
    ("company_id", (
        "id",
        "name"
    )),
    ("maintenance_team_id", (
        "id",
        "name"
    )),
    "description",
    ("stage_id", (
        "id",
        "name"
    )),
    "date_process",
    "schedule_date",
    "odometer_maintenance",
    ("attachment_ids", [(
        "url",
    )]),
)

OUT_model_res_user_create_one_SCHEMA = (
    "id",
    "name",
    "login",
)

OUT_fleet_product_schema = (
    "id",
    "name",
)


class ControllerREST(http.Controller):

    @http.route('/api/res.users', methods=['POST'], type='http', auth='none', cors=rest_cors_value, csrf=False)
    # @check_permissions
    def api_model_res_users_POST(self, **kw):
        data = json.loads(request.httprequest.data)
        register_token = data.get("register_token")
        if not register_token:
            return error_response(400, 'Error', 'Register token is required!')
        company_id = http.request.env.ref('base.main_company')
        token = company_id.token_register_account
        if not token or token != register_token:
            return error_response(400, 'Error', 'Token is invalid!')

        name, email, password = data.get('name'), data.get('email'), data.get('password')
        if not name or not email or not password:
            return error_response(400, 'Error', 'All fields must be filled out!')
        user_obj = request.env['res.users'].with_user(SUPERUSER_ID)

        already_email = user_obj.search([("login", "=", email)])

        if already_email:
            return error_response(400, 'Error', 'Account already exists!')

        access_token = user_obj.create_by_api(name, email, password, company_id)
        return successful_response(201, {'success': True, 'access_token': access_token})

    @http.route('/api/maintenance.equipment', methods=['GET'], type='http', auth='none', cors=rest_cors_value)
    @check_permissions
    def api_maintenance_equipment_GET(self, **kw):
        domain = []
        for key, val in request.httprequest.args.items():
            try:
                val = literal_eval(val)
            except:
                pass
            domain += [(key, '=', val)]
        return wrap_resource_read_all(
            modelname='maintenance.equipment',
            default_domain=domain or [],
            success_code=OUT_SUCCESS_CODE,
            OUT_fields=OUT_maintenance_equipment_schema,
            search_more=True)

    @http.route('/api/maintenance.equipment/<id>', methods=['GET'], type='http', auth='none', cors=rest_cors_value)
    @check_permissions
    def api_model_maintenance_equipment_id_GET(self, id, **kw):
        return wrap_resource_read_one(
            modelname='maintenance.equipment',
            id=id,
            success_code=OUT_SUCCESS_CODE,
            OUT_fields=OUT_maintenance_equipment_schema
        )

    @http.route('/api/maintenance.request', methods=['GET'], type='http', auth='none', cors=rest_cors_value)
    @check_permissions
    def api_maintenance_request_GET(self, **kw):
        domain = []
        for key, val in request.httprequest.args.items():
            try:
                val = literal_eval(val)
            except:
                pass
            domain += [(key, '=', val)]
        return wrap_resource_read_all(
            modelname='maintenance.request',
            default_domain=domain or [],
            success_code=OUT_SUCCESS_CODE,
            OUT_fields=OUT_maintenance_request_schema,
            order_data='date_process desc')

    @http.route('/api/maintenance.equipment/<id>/<method>', methods=['PUT'], type='http', auth='none',
                cors=rest_cors_value,
                csrf=False)
    @check_permissions
    def api_maintenance_equipment_method_PUT(self, id, method, **kw):
        return wrap_resource_call_method(
            modelname='maintenance.equipment',
            id=id,
            method=method,
            success_code=OUT_SUCCESS_CODE
        )

    @http.route('/api/res.users/<id>', methods=['GET'], type='http', auth='none', cors=rest_cors_value)
    @check_permissions
    def api_model_res_users_id_GET(self, id, **kw):
        return wrap_resource_read_one(
            modelname='res.users',
            id=id,
            success_code=OUT_SUCCESS_CODE,
            OUT_fields=OUT_model_res_user_read_one_SCHEMA
        )

    @http.route('/api/fleet.trip', methods=['GET'], type='http', auth='none', cors=rest_cors_value)
    @check_permissions
    def api_model_fleet_trip_GET(self, **kw):
        domain = []
        today = datetime.date.today().strftime('%Y-%m-%d')
        for key, val in request.httprequest.args.items():
            try:
                val = literal_eval(val)
            except:
                pass
            if key == 'date':
                if val == 'today':
                    domain += [('schedule_date', '>=', today), ('schedule_date', '<=', today)]
                continue

            if key == 'from_date':
                if val:
                    domain += [('schedule_date', '>=', val)]
                continue
            if key == 'to_date':
                if val:
                    domain += [('schedule_date', '<=', val)]
                continue
            if key == 'state':
                if val:
                    domain += [('state', '=', val)]
                continue

            domain += [(key, '=', val)]
        return wrap_resource_read_all(
            modelname='fleet.trip',
            default_domain=domain or [],
            success_code=OUT_SUCCESS_CODE,
            OUT_fields=OUT_FLEET_TRIP_schema,
            order_data='create_date desc, state')

    @http.route('/api/fleet.trip/<id>/<method>', methods=['PUT'], type='http', auth='none',
                cors=rest_cors_value,
                csrf=False)
    @check_permissions
    def api_model_fleet_trip_method_PUT(self, id, method, **kw):
        return wrap_resource_call_method(
            modelname='fleet.trip',
            id=id,
            method=method,
            success_code=OUT_SUCCESS_CODE
        )

    @http.route('/api/province', methods=['GET'], type='http', auth='none', csrf=False, cors=rest_cors_value)
    @check_permissions
    def api_model_province_info_id_GET(self, **kw):
        return wrap_resource_read_all(
            modelname="res.country.state",
            default_domain=[('country_id', '=', 241)],
            success_code=200,
            OUT_fields=OUT_address_schema,
        )

    @http.route('/api/district', methods=['GET'], type='http', auth='none', csrf=False, cors=rest_cors_value)
    @check_permissions
    def api_model_district_info_id_GET(self, **kw):
        domain = []
        for key, val in request.httprequest.args.items():
            try:
                val = literal_eval(val)
            except:
                pass
            if not val:
                continue
            domain += [(key, '=', val)]
        return wrap_resource_read_all(
            modelname="res.country.district",
            default_domain=domain or [],
            success_code=200,
            OUT_fields=OUT_address_schema,
        )

    @http.route('/api/ward', methods=['GET'], type='http', auth='none', csrf=False, cors=rest_cors_value)
    @check_permissions
    def api_model_ward_info_id_GET(self, **kw):
        domain = []
        for key, val in request.httprequest.args.items():
            try:
                val = literal_eval(val)
            except:
                pass
            if not val:
                continue
            domain += [(key, '=', val)]
        return wrap_resource_read_all(
            modelname="res.country.ward",
            default_domain=domain or [],
            success_code=200,
            OUT_fields=OUT_address_schema,
        )

    @http.route('/api/fleet.location', methods=['GET'], type='http', auth='none', csrf=False, cors=rest_cors_value)
    @check_permissions
    def api_model_fleet_location_id_GET(self, **kw):
        domain = []
        for key, val in request.httprequest.args.items():
            try:
                val = literal_eval(val)
            except:
                pass
            if not val:
                continue
            domain += [(key, '=', val)]
        return wrap_resource_read_all(
            modelname="fleet.location",
            default_domain=domain or [],
            success_code=200,
            OUT_fields=OUT_fleet_location_schema,
        )

    @http.route('/api/fleet.trip', methods=['POST'], type='http', auth='none', cors=rest_cors_value, csrf=False)
    @check_permissions
    def api_model_fleet_trip_POST(self, **kw):
        employee_id = False
        if request.httprequest.data:
            employee_id = json.loads(request.httprequest.data).get('employee_id')
        if not employee_id:
            uid = request.session.uid
            employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', uid)])
            employee_id = employee_id.id if employee_id else False
        return wrap_resource_create_one(
            modelname='fleet.trip',
            default_vals={'country_id': 241, 'employee_id': employee_id},
            success_code=200,
            OUT_fields=OUT_FLEET_TRIP_schema
        )

    @http.route('/api/fleet.trip/<id>', methods=['GET'], type='http', auth='none', cors=rest_cors_value)
    @check_permissions
    def api_model_fleet_trip_id_GET(self, id, **kw):
        return wrap_resource_read_one(
            modelname='fleet.trip',
            id=id,
            success_code=OUT_SUCCESS_CODE,
            OUT_fields=OUT_FLEET_TRIP_schema
        )

    @http.route('/api/fleet.product', methods=['GET'], type='http', auth='none', cors=rest_cors_value)
    @check_permissions
    def api_fleet_product_GET(self, **kw):
        domain = []
        for key, val in request.httprequest.args.items():
            try:
                val = literal_eval(val)
            except:
                pass
            domain += [(key, '=', val)]
        return wrap_resource_read_all(
            modelname='fleet.product',
            default_domain=domain or [],
            success_code=OUT_SUCCESS_CODE,
            OUT_fields=OUT_fleet_product_schema,
            search_more=True)
