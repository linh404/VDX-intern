from datetime import timedelta
from typing import Reversible
from odoo import fields, models, api
from odoo.api import IdType
from odoo.exceptions import UserError


# Mentor Q8
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _rec_name = "name"

    name = fields.Char(default="")
    price = fields.Float()
    create_date = fields.Date(default=lambda self: fields.Date.today())
    status = fields.Selection(
        [
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
        default="pending"
    )

    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    # Mentor Q5/Q17; Mentor Q23
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )

    # Inverse
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        # Mentor Q6/Q9
        for record in self:
            create_date = fields.Date.to_date(record.create_date) or fields.Date.context_today(record)
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(record.create_date) or fields.Date.context_today(record)
            if record.date_deadline:
                record.validity = (record.date_deadline - create_date).days

    # override method
    @api.model_create_multi
    def create(self, vals_list):
        # Mentor Q9
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == "new":
                offer.property_id.sudo().state = "offer_received"
        return offers

    # action func
    def action_accept(self):
        for record in self:
            if record.property_id.state in ("sold", "cancelled"):
                raise UserError(self.env._("You cannot accept an offer for a sold or cancelled property."))
            accepted_offer = record.property_id.offer_ids.filtered(
                lambda offer: offer.status == "accepted" and offer != record
            )

            if accepted_offer:
                raise UserError(self.env._("Only one offer can be accepted for a property."))
            other_offers = record.property_id.offer_ids - record
            other_offers.filtered(lambda offer: offer.status != "refused").action_refuse()
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            if record.property_id.state in ("sold", "cancelled"):
                raise UserError(self.env._("You cannot refuse an offer for a sold or canceled property."))
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
