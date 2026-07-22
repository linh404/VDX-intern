from odoo import fields, models


# Mentor Q8
class EstatePropertyCancelWizard(models.TransientModel):
    _name = "estate.property.cancel.wizard"
    _description = "Estate Property Cancel Wizard"

    property_id = fields.Many2one(
        "estate.property",
        required=True,
    )
    reason = fields.Text(string="Cancel Reason")

    def action_confirm_cancel(self):
        for wizard in self:
            wizard.property_id.cancel_reason = wizard.reason
            wizard.property_id.action_cancel()
        # Mentor Q25
        return {"type": "ir.actions.act_window_close"}
