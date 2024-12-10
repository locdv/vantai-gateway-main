from odoo import api, fields, models, _
import datetime
import qrcode
import base64
import io
import requests


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    license_plate = fields.Char(related='vehicle_id.license_plate', string='Biển số', required=False)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Phương tiện')
    department_belong_id = fields.Many2one('hr.department', string="Thuộc đơn vị")
    model_id = fields.Many2one('fleet.vehicle.model',related='vehicle_id.model_id', string="Nhãn xe")
    fuel_id = fields.Many2one('product.template', string='Nhiên liệu')
    number_seat = fields.Integer('Số ghế')
    quota = fields.Integer('Định mức')
    location_id = fields.Many2one('fleet.location', string="Vị Trí cất xe")
    district_id = fields.Many2one('res.country.district', string='Huyện', domain="[('state_id', '=', state_id)]")
    ward_id = fields.Many2one('res.country.ward', string='Xã', domain="[('district_id', '=', district_id)]")
    state_id = fields.Many2one("res.country.state", string='Tỉnh', ondelete='restrict',
                               domain="[('country_id', '=', country_id)]")
    address_start = fields.Char(string="Địa chỉ xuất phát")
    @api.onchange("location_id")
    def onchange_location_id(self):
        if self.location_id:
            # self.location_name = self.location_id.name
            self.district_id = self.location_id.district_id.id
            self.ward_id = self.location_id.ward_id.id
            self.state_id = self.location_id.state_id.id
            self.address_start = self.location_id.note 
            
    def name_get(self):
        self.browse(self.ids).read(['name', 'license_plate'])
        return [(car.id, '%s' % car.license_plate if car.license_plate else '-') for car in self]

    qr_code = fields.Char(string="Mã QR", copy=False, compute='_get_qr_code')
    qr_code_img = fields.Binary(string="Hình ảnh QR", copy=False, compute='_get_qr_code')
    last_request = fields.Date(string='Yêu cầu gần nhất', compute='_get_last_request', store=True)
    trip_ids = fields.One2many('fleet.trip', 'equipment_id')
    trip_count = fields.Integer(string='Số chuyến hôm nay', compute='_compute_trip_count')
    message_ids = fields.One2many('mail.message', 'res_id', string='Ghi chú')

    @api.depends('trip_ids')
    def _compute_trip_count(self):
        for rec in self:
            today = datetime.date.today()
            rec.trip_count = len(rec.trip_ids.filtered(lambda x: x.schedule_date == today))

    @api.depends('maintenance_ids', 'maintenance_ids.date_process')
    def _get_last_request(self):
        for rec in self:
            last_request = rec.maintenance_ids.filtered(lambda x: x.date_process)
            last_request = last_request.sorted(key=lambda r: r.date_process, reverse=True)
            rec.last_request = last_request[0].date_process if last_request else False

    @api.depends('license_plate')
    def _get_qr_code(self):
        for rec in self:
            if not rec.license_plate:
                rec.qr_code = False
                rec.qr_code_img = False
            else:
                rec.qr_code = rec.license_plate
                rec.qr_code_img = rec.get_qr_code(rec.license_plate)

    def get_qr_code(self, data):
        if data != "":
            img = qrcode.make(data)
            result = io.BytesIO()
            img.save(result, format='PNG')
            result.seek(0)
            img_bytes = result.read()
            base64_encoded_result_bytes = base64.b64encode(img_bytes)
            base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
            return base64_encoded_result_str

    def create_maintenance_request(self, note, odometer_maintenance, attachments=[]):

        vals = {
            'equipment_id': self.id,
            'name': f'Yêu cầu sửa chữa xe {self.name} - {self.license_plate}',
            'description': note,
            'odometer_maintenance': odometer_maintenance,
        }
        maintenance_request = self.env['maintenance.request'].create(vals)
        if not attachments:
            return maintenance_request
        for attachment in attachments:
            self.env['ir.attachment'].create({
                'name': maintenance_request.name,
                'type': 'url',
                'url': attachment,
                'res_model': 'maintenance.request',
                'res_id': maintenance_request.id,
            })
        return maintenance_request


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    date_process = fields.Date(string='Ngày thực hiện')
    odometer_maintenance = fields.Float(string="Số KM bảo trì")
    attachment_ids = fields.One2many('ir.attachment', 'res_id',
                                     domain=[('res_model', '=', 'maintenance.request')],
                                     string='Attachments')
