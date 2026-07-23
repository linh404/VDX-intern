from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_is_zero, float_compare


# Mentor Q8
class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin"]
    _description = 'My Estate Property'
    _order = "id desc"
    _rec_name = "name"
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )
    _check_selling_price_non_negative = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive.",
    )
    name = fields.Char(string="Estate Property", required=True)
    description = fields.Text()
    internal_note = fields.Text(copy=False)
    cancel_reason = fields.Text(copy=False)
    postcode = fields.Char()
    # Mentor Q29
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(required=True, tracking=True)
    selling_price = fields.Float(
        required=True,
        copy=False,
        default="0",
        tracking=True,
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    # Mentor Q24
    active = fields.Boolean(default=True)

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
        tracking=True,
    )

    # Mentor Q28
    # Mentor Q5/Q17
    property_type_id = fields.Many2one("estate.property.type")

    buyer_id = fields.Many2one("res.partner", copy=False, tracking=True)
    salesperson_id = fields.Many2one(
        "res.users",
        default=lambda self: self.env.user,
        tracking=True,
    )

    tag_ids = fields.Many2many(
        "estate.property.tag",
    )

    # Mentor Q23
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
    )

    # Computed, Onchange
    # Mentor Q11; Mentor Q22
    total_area = fields.Integer(compute="_compute_total_area")
    # Mentor Q7/Q10/Q11; Mentor Q22
    best_price = fields.Float(
        compute="_compute_best_price",
        store=True
    )

    def _compute_access_url(self):
        result = super()._compute_access_url()
        for record in self:
            record.access_url = f"/estate/property/{record.id}"
        return result

    def write(self, vals):
        result = super().write(vals)

        if "internal_note" in vals:
            for record in self:
                record.message_post(
                    body=self.env._("Internal note was updated.")
                )

        return result

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        # Mentor Q6/Q9
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        # Mentor Q6/Q9
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        # Mentor Q6/Q9
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # Mentor Q33
    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(self.env._("A cancelled property cannot be sold."))
            record.state = "sold"
        return True

    # Mentor Q33
    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(self.env._("A sold property cannot be cancelled."))
            if record.offer_ids.filtered(lambda offer: offer.status == "accepted"):
                raise UserError(self.env._("A property with an accepted offer cannot be cancelled."))
            record.offer_ids.filtered(
                lambda offer: offer.status != "refused"
            ).action_refuse()
            record.state = "cancelled"
        return True

    def action_open_cancel_wizard(self):
        self.ensure_one()
        # Mentor Q13/Q18/Q25/Q33
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Cancel Property"),
            "res_model": "estate.property.cancel.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_property_id": self.id,
            },
        }

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price_ratio(self):
        for record in self:
            # selling_price = 0 means the property has not been sold yet.
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue

            minimum_price = record.expected_price * 0.9

            if float_compare(
                    record.selling_price,
                    minimum_price,
                    precision_rounding=0.01,
            ) < 0:
                raise ValidationError(
                    self.env._("The selling price cannot be lower than 90% of the expected price.")
                )

    def action_cancel_draft(self):
        # Mentor Q25
        sold_properties = self.filtered(
            lambda property_record:
            property_record.state == "sold"
        )

        if sold_properties:
            raise UserError(
                self.env._("A sold property cannot be cancelled.")
            )

        self.write({
            "state": "cancelled",
        })

