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

        # Mentor Q25/Q30
        html = request.env["ir.actions.report"]._render_qweb_html(
            REPORT_NAME,
            [property_record.id],
        )[0]
        return request.make_response(html)

    # HTTP return type examples
    @http.route(
        "/estate/http-return/<string:return_type>",
        type="http",
        auth="user",
        website=True,
        readonly=True,
        methods=["GET"],
    )
    def http_return_example(self, return_type):
        if return_type == "string":
            return """
                <h1>HTTP string return</h1>
                <p>This response is returned directly as a string.</p>
            """

        if return_type == "render":
            properties = request.env["estate.property"].search([], limit=20)
            return request.render(
                LIST_PROPERTY_NAME,
                {
                    "properties": properties,
                },
            )

        if return_type == "response":
            return request.make_response(
                """
                    <h1>HTTP response return</h1>
                    <p>This response is built with request.make_response().</p>
                """,
                headers=[
                    ("Content-Type", "text/html; charset=utf-8"),
                    ("X-Estate-Return-Type", "response"),
                ],
            )

        if return_type == "redirect":
            return request.redirect("/estate/properties")

        raise NotFound()

    # JSON-2 + Bearer API key
    @http.route(
        "/my_estate/properties",
        type="json2",
        auth="bearer",
        readonly=True,
        methods=["POST"],
        save_session=False,
    )
    def properties(self, state=None):
        domain = []
        if state:
            domain.append(("state", "=", state))

        properties = request.env["estate.property"].search(domain, limit=20)
        return {
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
