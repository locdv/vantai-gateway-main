# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class FleetProject(models.Model):
    _name = 'fleet.project'
    _description = 'Dự án'
    _order = 'name'

    name = fields.Char(string='Tên dự án', required=True)


class FleetCategory(models.Model):
    _name = 'fleet.category'
    _description = 'Hạng mục'
    _order = 'name'

    name = fields.Char(string='Tên hạng mục', required=True)


class FleetLocation(models.Model):
    _name = 'fleet.location'
    _description = 'Địa điểm'
    _order = 'name'

    name = fields.Char(string='Tên vị trí', required=True)
    code = fields.Char(readonly=True)
    district_id = fields.Many2one('res.country.district', string='Huyện', domain="[('state_id', '=', state_id)]")
    ward_id = fields.Many2one('res.country.ward', string='Xã', domain="[('district_id', '=', district_id)]")
    state_id = fields.Many2one("res.country.state", string='Tỉnh', ondelete='restrict',
                               domain="[('country_id', '=', country_id)]")
    country_id = fields.Many2one('res.country', default=241, string='Quốc gia', ondelete='restrict')
    note = fields.Text(string="Ghi chú")

    @api.model
    def create(self, vals_list):
        district_id = vals_list.get('district_id', False)
        ward_id = vals_list.get('ward_id', False)
        state_id = vals_list.get('state_id', False)
        note = vals_list.get('note', False)
        num_location = self.env['fleet.location'].search(
            [('district_id', '=', district_id),
             ('ward_id', '=', ward_id),
             ('state_id', '=', state_id),
             ('note', '=', note)])
        if num_location:
            raise ValidationError('Không thể tạo địa điểm trùng nhau!')
        return super(FleetLocation, self).create(vals_list)


# class FleetCar(models.Model):
#     _name = 'fleet.car'
#     _description = 'Phương Tiện'
#     _order = 'name'
#
#     name = fields.Char(string='Tên phương tiện', required=True)
#     license_plate = fields.Char(string='Biển số', required=True)
#     acquisition_date = fields.Date('Ngày đăng kiểm')
#     vin_sn = fields.Char('Số khung', copy=False)
#     seats = fields.Integer('Số ghế')
#     model_year = fields.Char('Đời xe')
#     color = fields.Char('Màu xe')
#
#     fleet_trip_ids = fields.One2many('fleet.trip', 'car_id', 'Danh sách hành trình', readonly=True)
#
#     def name_get(self):
#         self.browse(self.ids).read(['name', 'license_plate'])
#         return [(car.id, '%s%s' % (car.license_plate and '[%s] ' % car.license_plate or '', car.name))
#                 for car in self]


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    section = fields.Char(string='Tiết diện')
    product_length = fields.Integer(string='Dài')


class FleetProduct(models.Model):
    _name = 'fleet.product'
    _description = 'Mặt hàng'
    _order = 'name'

    name = fields.Char(string='Tên mặt hàng', required=True)
    

class FleetRoute(models.Model):
    _name = 'fleet.route'
    _description = 'Cung Đường'
    _order = 'name'

    name = fields.Char(string='Tên cung đường', required=True)
    start_location_id = fields.Many2one('fleet.location', string='Điểm bắt đầu', required=True)
    end_location_id = fields.Many2one('fleet.location', string='Điểm kết thúc', required=True)
    description = fields.Text(string='Mô tả cung đường')
    note = fields.Text(string='Ghi chú')
    estimated_km = fields.Float(string='Số km dự kiến')

    @api.model
    def create(self, vals_list):
        # Custom logic for route creation if needed
        return super(FleetRoute, self).create(vals_list)

