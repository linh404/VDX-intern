from odoo import http
from odoo.http import content_disposition, request
from werkzeug.exceptions import NotFound


REPORT_NAME = "my_estate.report_estate_property"


class EstatePropertyReportController(http.Controller):
    @http.route(
        [
            "/estate/property/<int:property_id>/report",
            "/estate/property/<int:property_id>/report/<string:report_type>",
        ],
        type="http",
        auth="public",
        website=True,
        readonly=True,
        methods=["GET"],
    )
    def estate_property_report(self, property_id, report_type="pdf", download=False, **kwargs):
        property_record = (
            request.env["estate.property"]
            .sudo()
            .browse(property_id)
            .exists()
        )
        if not property_record:
            raise NotFound()
        if report_type not in ("html", "pdf"):
            raise NotFound()

        report = request.env["ir.actions.report"].sudo()
        if report_type == "html":
            html = report._render_qweb_html(
                REPORT_NAME,
                [property_record.id],
            )[0]
            return request.make_response(html)

        pdf = report._render_qweb_pdf(
            REPORT_NAME,
            [property_record.id],
        )[0]
        filename = f"Estate Property - {property_record.name}.pdf"
        disposition_type = "attachment" if self._to_bool(download) else "inline"
        headers = [
            ("Content-Type", "application/pdf"),
            ("Content-Length", len(pdf)),
            (
                "Content-Disposition",
                content_disposition(filename, disposition_type=disposition_type),
            ),
        ]
        return request.make_response(pdf, headers=headers)

    def _to_bool(self, value):
        return str(value).lower() in ("1", "true", "yes", "on")
