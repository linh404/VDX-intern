from datetime import timedelta

from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )

    # Inverse
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(record.create_date) or fields.Date.context_today(record)
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(record.create_date) or fields.Date.context_today(record)
            if record.date_deadline:
                record.validity = (record.date_deadline - create_date).days
