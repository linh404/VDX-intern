from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound


REPORT_NAME = "my_estate.report_estate_property"
LIST_PROPERTY_NAME = "my_estate.estate_property_list"

class EstatePropertyController(http.Controller):
    # List property
    @http.route(
        "/estate/properties",
        type="http",
        auth="user",
        website=True,
        readonly=True,
        methods=["GET"],
    )
    def property_list(self):
        properties = request.env["estate.property"].search([])
        return request.render(
            LIST_PROPERTY_NAME,
            {
                "properties": properties,
            },
        )

    # Report property
    @http.route(
        "/estate/property/<int:property_id>/report",
        type="http",
        auth="user",
        website=True,
        readonly=True,
        methods=["GET"],
    )
    def property_report(self, property_id):
        property_record = request.env["estate.property"].browse(property_id).exists()
        if not property_record:
            raise NotFound()

        html = request.env["ir.actions.report"]._render_qweb_html(
            REPORT_NAME,
            [property_record.id],
        )[0]
        return request.make_response(html)

    # JSONRPC
    @http.route(
        "/my_estate/properties",
        type="jsonrpc",
        auth="user",
        methods=["POST"],
    )
    def properties(self, state=None):
        domain = []
        if state:
            domain.append(("state", "=", state))

        properties = request.env["estate.property"].search(domain, limit=20)
        return {
            "count": len(properties),
            "properties": [
                {
                    "id": property_record.id,
                    "name": property_record.name,
                    "state": property_record.state,
                    "expected_price": property_record.expected_price,
                    "best_price": property_record.best_price,
                }
                for property_record in properties
            ],
        }
