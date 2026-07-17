from odoo import fields, http
from odoo.exceptions import UserError
from odoo.http import request


class EstatePropertyApiController(http.Controller):
    @http.route(
        "/my_estate/properties",
        type="jsonrpc",
        auth="user",
        methods=["POST"],
    )
    def get_properties(self, state=None, search=None, limit=20, offset=0):
        domain = []
        if state:
            domain.append(("state", "=", state))
        if search:
            domain.append(("name", "ilike", search))

        properties = request.env["estate.property"].search(
            domain,
            limit=min(int(limit), 100),
            offset=int(offset),
        )

        return {
            "count": len(properties),
            "properties": [
                self._serialize_property(property_record)
                for property_record in properties
            ],
        }

    @http.route(
        "/my_estate/properties/<int:property_id>",
        type="jsonrpc",
        auth="user",
        methods=["POST"],
    )
    def get_property(self, property_id):
        property_record = request.env["estate.property"].search(
            [("id", "=", property_id)],
            limit=1,
        )
        if not property_record:
            return {"error": "property_not_found"}

        return self._serialize_property(property_record, include_offers=True)

    @http.route(
        "/my_estate/properties/<int:property_id>/offers",
        type="jsonrpc",
        auth="user",
        methods=["POST"],
    )
    def create_offer(self, property_id, partner_id=None, price=None, validity=None):
        property_record = request.env["estate.property"].search(
            [("id", "=", property_id)],
            limit=1,
        )
        if not property_record:
            return {"error": "property_not_found"}
        if not partner_id:
            raise UserError(request.env._("Partner is required."))
        if price is None:
            raise UserError(request.env._("Offer price is required."))

        vals = {
            "property_id": property_record.id,
            "partner_id": int(partner_id),
            "price": float(price),
        }
        if validity is not None:
            vals["validity"] = int(validity)

        offer = request.env["estate.property.offer"].create(vals)
        return {
            "offer": self._serialize_offer(offer),
            "property": self._serialize_property(property_record),
        }

    def _serialize_property(self, property_record, include_offers=False):
        data = {
            "id": property_record.id,
            "name": property_record.name,
            "description": property_record.description,
            "postcode": property_record.postcode,
            "date_availability": fields.Date.to_string(property_record.date_availability),
            "expected_price": property_record.expected_price,
            "selling_price": property_record.selling_price,
            "bedrooms": property_record.bedrooms,
            "living_area": property_record.living_area,
            "facades": property_record.facades,
            "garage": property_record.garage,
            "garden": property_record.garden,
            "garden_area": property_record.garden_area,
            "garden_orientation": property_record.garden_orientation,
            "total_area": property_record.total_area,
            "best_price": property_record.best_price,
            "state": property_record.state,
            "property_type": self._serialize_many2one(property_record.property_type_id),
            "buyer": self._serialize_many2one(property_record.buyer_id),
            "salesperson": self._serialize_many2one(property_record.salesperson_id),
            "tags": [
                {
                    "id": tag.id,
                    "name": tag.name,
                }
                for tag in property_record.tag_ids
            ],
        }
        if include_offers:
            data["offers"] = [
                self._serialize_offer(offer)
                for offer in property_record.offer_ids
            ]
        return data

    def _serialize_offer(self, offer):
        return {
            "id": offer.id,
            "price": offer.price,
            "partner": self._serialize_many2one(offer.partner_id),
            "property_id": offer.property_id.id,
            "status": offer.status,
            "validity": offer.validity,
            "date_deadline": fields.Date.to_string(offer.date_deadline),
        }

    def _serialize_many2one(self, record):
        if not record:
            return False
        return {
            "id": record.id,
            "name": record.display_name,
        }
