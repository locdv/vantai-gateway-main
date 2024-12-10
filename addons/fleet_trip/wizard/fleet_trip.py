# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class FleetTripWizard(models.TransientModel):

    _name = 'fleet.trip.wizard'

    date_from = fields.Date(string='Từ ngày')
    date_to = fields.Date(string='Đến ngày')

    def generate_trip_report(self):
        trip_report = self.env['fleet.trip.report']
        trip_report.search([]).unlink()

        fleet_trip = self.env['fleet.trip'].search([
            ('schedule_date', '>=', self.date_from),
            ('schedule_date', '<=', self.date_to)])
        if not fleet_trip:
            raise ValidationError('Không có dữ liệu!')
        for rec in fleet_trip:
            vals = {
                'company_id': rec.company_id.id,
                'equipment_id': rec.equipment_id.id,
                'location_id': rec.location_id.id,
                'location_dest_id': rec.location_dest_id.id,
                'eating_fee': rec.eating_fee,
                'law_money': rec.law_money,
                'road_tiket_fee': rec.road_tiket_fee,
                'incurred_fee': rec.incurred_fee,
                'note': rec.note,
                'fee_total': rec.fee_total,
                'project_id': rec.project_id.id,
                'schedule_date_day': str(rec.schedule_date.strftime("%d")),
                'schedule_date_month': str(rec.schedule_date.strftime("%m")),
                'schedule_date_year': str(rec.schedule_date.strftime("%Y")),
                'trip_count': 1}
        trip_report.create(vals)

        return {
            'type': 'ir.actions.act_window',
            'target': 'current',
            'name': f'Bảng tổng hợp giám đốc ( {self.date_from} - {self.date_to})',
            'view_mode': 'tree',
            'view_id': self.env.ref('fleet_trip.fleet_trip_tree_report_view').id,
            'context': {'no_breadcrumbs': True},
            'res_model': 'fleet.trip.report',
        }


class FleetTripReport(models.TransientModel):

    _name = 'fleet.trip.report'

    company_id = fields.Many2one('res.company', 'Công ty')
    equipment_id = fields.Many2one('maintenance.equipment', string='Xe')
    license_plate = fields.Char(related='equipment_id.license_plate')
    location_id = fields.Many2one('fleet.location', 'Điểm xuất phát')
    location_dest_id = fields.Many2one('fleet.location', 'Điểm đích')
    eating_fee = fields.Float('Tiền ăn')
    law_money = fields.Float('Tiền luật')
    road_tiket_fee = fields.Float('Vé cầu đường')
    incurred_fee = fields.Float('Phát sinh')
    note = fields.Text('Ghi chú sửa chữa')
    fee_total = fields.Float('Tổng cộng')
    project_id = fields.Many2one('fleet.project', string='Dự án')
    schedule_date_day = fields.Char(string='Ngày')
    schedule_date_month = fields.Char(string='Tháng')
    schedule_date_year = fields.Char(string='Năm')

    fee_total_without_invoice = fields.Float(string='Tổng chưa hóa đơn')
    fee_invoice = fields.Float(string='Hóa đơn')
    fee_oil = fields.Float(string='Tiền dầu')
    fee_machine = fields.Float(string='Tiền máy')
    trip_length = fields.Integer(string='Chiều dài cung đường')
    trip_count = fields.Integer(string='Chuyến đi')