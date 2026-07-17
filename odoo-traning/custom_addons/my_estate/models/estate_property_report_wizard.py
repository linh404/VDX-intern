from odoo import fields, models


class EstatePropertyReportWizard(models.TransientModel):
    _name = "estate.property.report.wizard"
    _description = "Estate Property Report Wizard"

    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        readonly=True,
    )

    def action_print_report(self):
        self.ensure_one()
        return self.env.ref("my_estate.action_report_estate_property").report_action(
            self.property_id
        )
