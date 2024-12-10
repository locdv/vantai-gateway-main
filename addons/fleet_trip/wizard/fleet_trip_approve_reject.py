# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FleetTripApproveReject(models.TransientModel):
    _name = 'fleet.trip.approve.reject'

    fleet_trip_id = fields.Many2one("fleet.trip", string="Fleet Trip")

    def action_approve(self):
        self.fleet_trip_id.is_approved = True

    def action_reject(self):
        self.fleet_trip_id.unlink()
