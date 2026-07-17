from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound


class EstatePropertyWebsiteController(http.Controller):
    @http.route(
        "/estate/properties",
        type="http",
        auth="public",
        website=True,
        methods=["GET"],
    )
    def estate_property_list(self, **kwargs):
        properties = request.env["estate.property"].sudo().search([])

        return request.render(
            "my_estate.estate_property_list",
            {
                "properties": properties,
            },
        )

    @http.route(
        "/estate/property/<int:property_id>",
        type="http",
        auth="public",
        website=True,
        methods=["GET"],
    )
    def estate_property_detail(self, property_id, offer_created=None, **kwargs):
        property_record = request.env["estate.property"].sudo().search(
            [("id", "=", property_id)],
            limit=1,
        )
        if not property_record:
            raise NotFound()

        access_token = property_record._portal_ensure_token()

        return request.render(
            "my_estate.estate_property_detail",
            {
                "estate_property": property_record,
                "offer_created": bool(offer_created),
                "access_token": access_token,
            },
        )

    @http.route(
        "/estate/offer/new",
        type="http",
        auth="public",
        website=True,
        methods=["GET"],
    )
    def estate_offer_new(self, property_id=None, **kwargs):
        selected_property = self._get_available_property(property_id)
        return request.render(
            "my_estate.estate_offer_form",
            self._get_offer_form_values(selected_property=selected_property),
        )

    @http.route(
        "/estate/offer",
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
    )
    def estate_offer_submit(self, **post):
        errors = {}
        property_record = self._get_available_property(post.get("property_id"))
        if not property_record:
            errors["property_id"] = request.env._("Please choose an available property.")

        partner_name = (post.get("partner_name") or "").strip()
        partner_email = (post.get("partner_email") or "").strip()
        if not partner_name:
            errors["partner_name"] = request.env._("Your name is required.")

        price = self._parse_positive_float(
            post.get("price"),
            "price",
            request.env._("Offer price must be strictly positive."),
            errors,
        )
        validity = self._parse_optional_positive_int(
            post.get("validity"),
            "validity",
            request.env._("Validity must be a positive number of days."),
            errors,
        )

        if errors:
            return request.render(
                "my_estate.estate_offer_form",
                self._get_offer_form_values(
                    form=post,
                    errors=errors,
                    selected_property=property_record,
                ),
            )

        partner = self._get_or_create_offer_partner(partner_name, partner_email)
        offer_values = {
            "property_id": property_record.id,
            "partner_id": partner.id,
            "price": price,
        }
        if validity is not None:
            offer_values["validity"] = validity

        request.env["estate.property.offer"].sudo().create(offer_values)
        return request.redirect(f"/estate/property/{property_record.id}?offer_created=1")

    def _get_available_property(self, property_id):
        property_id = self._to_int(property_id)
        if not property_id:
            return request.env["estate.property"].browse()

        return request.env["estate.property"].sudo().search(
            [
                ("id", "=", property_id),
                ("state", "not in", ["sold", "cancelled"]),
            ],
            limit=1,
        )

    def _get_offer_form_values(self, form=None, errors=None, selected_property=None):
        properties = request.env["estate.property"].sudo().search(
            [("state", "not in", ["sold", "cancelled"])],
        )
        form = form or {}
        selected_property_id = (
            selected_property.id
            if selected_property
            else self._to_int(form.get("property_id"))
        )

        return {
            "properties": properties,
            "selected_property_id": selected_property_id,
            "form": form,
            "errors": errors or {},
        }

    def _get_or_create_offer_partner(self, name, email):
        Partner = request.env["res.partner"].sudo()
        if email:
            partner = Partner.search([("email", "=", email)], limit=1)
            if partner:
                return partner

        return Partner.create(
            {
                "name": name,
                "email": email,
            }
        )

    def _parse_positive_float(self, value, field_name, error_message, errors):
        try:
            parsed_value = float(value or 0)
        except (TypeError, ValueError):
            parsed_value = 0

        if parsed_value <= 0:
            errors[field_name] = error_message
        return parsed_value

    def _parse_optional_positive_int(self, value, field_name, error_message, errors):
        if not value:
            return None

        try:
            parsed_value = int(value)
        except (TypeError, ValueError):
            parsed_value = 0

        if parsed_value <= 0:
            errors[field_name] = error_message
        return parsed_value

    def _to_int(self, value):
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0
