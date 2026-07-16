from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"
    _rec_name = "name"
    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The tag name must be unique.",
    )

    name = fields.Char(required=True)


