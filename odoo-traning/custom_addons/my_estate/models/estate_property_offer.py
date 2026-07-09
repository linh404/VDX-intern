from datetime import timedelta
from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _rec_name = "name"

    name = fields.Char(default="Test _rec_name")
    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )

    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
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

    # action func
    def action_accept(self):
        for record in self:
            accepted_offer = record.property_id.offer_ids.filtered(
                lambda offer: offer.status == "accepted" and offer != record
            )

            if accepted_offer:
                raise UserError("Only one offer can be accepted for a property.")

            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True

    # constraints
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]
