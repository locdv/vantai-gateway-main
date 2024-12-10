from odoo import api, fields, models
from odoo.exceptions import ValidationError

SQL_GENERATE_FLEET_TRIP_COST_REPORT = """
DELETE FROM fleet_trip_cost_report WHERE id is not null;
INSERT INTO fleet_trip_cost_report
(schedule_date, equipment_id, source, amount, note, create_uid)
SELECT REPORT.schedule_date AS schedule_date,
       REPORT.equipment_id  AS equipment_id,
       REPORT.source        AS source,
       REPORT.amount        AS amount,
       REPORT.note          AS note,
       REPORT.create_uid    AS create_uid
FROM ((SELECT FMR.date           AS schedule_date,
              FMR.equipment_id   AS equipment_id,
              'invoice'          AS source,
              FMR.invoice_amount AS amount,
              FMR.bill_content   AS note,
              FMR.create_uid     AS create_uid
       FROM fleet_main_report FMR
       WHERE FMR.date BETWEEN '{from_date}' AND '{to_date}')
      UNION ALL
      (SELECT FT.schedule_date   AS schedule_date,
              FT.equipment_id    AS equipment_id,
              'incurred_fee_2'   AS source,
              FT.incurred_fee_2  AS amount,
              FT.incurred_note_2 AS note,
              FT.create_uid      AS create_uid
       FROM fleet_trip FT
       WHERE FT.schedule_date BETWEEN '{from_date}' AND '{to_date}')) AS REPORT
ORDER BY REPORT.schedule_date, REPORT.equipment_id;
"""


class FleetTripCostGenerate(models.TransientModel):
    _name = 'fleet.trip.cost.generate'
    _description = 'Fleet Trip Cost Generate'

    from_date = fields.Date(string="Từ ngày", required=True)
    to_date = fields.Date(string="Đến Ngày", required=True)

    @api.onchange('from_date', 'to_date')
    def onchange_from_date_to_date(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu.")

    def action_generate_fleet_trip_cost_report(self):
        sql = SQL_GENERATE_FLEET_TRIP_COST_REPORT.format(
            create_uid=self._uid, from_date=self.from_date, to_date=self.to_date)
        self._cr.execute(sql)
        return self.action_view_fleet_trip_cost_report()

    @staticmethod
    def action_view_fleet_trip_cost_report():
        act_window = {
            'type': 'ir.actions.act_window',
            'name': "Bảng chi phí vận tải",
            'res_model': 'fleet.trip.cost.report',
            'view_mode': 'tree',
            'target': 'main',
        }
        return act_window


class FleetTripCostReport(models.Model):
    _name = 'fleet.trip.cost.report'
    _description = 'Fleet Trip Cost Report'

    schedule_date = fields.Date(string='Ngày')
    equipment_id = fields.Many2one('maintenance.equipment', string='Xe')
    source = fields.Selection(string="Nguồn",
                              selection=[('invoice', 'Hóa đơn'), ('incurred_fee_2', 'Phát sinh 2')])
    amount = fields.Float(string='Chi phí', digits=(16, 0))
    note = fields.Text(string="Nội dung hoá đơn")

