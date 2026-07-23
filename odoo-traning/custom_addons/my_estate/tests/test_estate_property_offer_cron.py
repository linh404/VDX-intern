from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestEstatePropertyOfferCron(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.Property = cls.env["estate.property"]
        cls.Offer = cls.env["estate.property.offer"]
        cls.partner = cls.env["res.partner"].create({
            "name": "Cron Test Buyer",
        })

    def _create_property(self, name):
        return self.Property.create({
            "name": name,
            "expected_price": 100000.0,
        })

    def _create_offer(self, property_record, **values):
        offer_values = {
            "property_id": property_record.id,
            "partner_id": self.partner.id,
            "price": 95000.0,
        }
        offer_values.update(values)
        return self.Offer.create(offer_values)

    def test_cron_record_targets_property_offer_model(self):
        cron = self.env.ref("my_estate.estate_property_offer_cron_refuse_expired")

        self.assertEqual(cron.model_id.model, "estate.property.offer")
        self.assertEqual(cron.interval_number, 1)
        self.assertEqual(cron.interval_type, "days")

    def test_cron_refuses_only_expired_pending_offers(self):
        expired_offer = self._create_offer(
            self._create_property("Expired offer property"),
            validity=-1,
        )
        current_offer = self._create_offer(
            self._create_property("Current offer property"),
            validity=7,
        )
        accepted_offer = self._create_offer(
            self._create_property("Accepted offer property"),
            validity=-1,
            status="accepted",
        )
        sold_property = self._create_property("Sold property")
        sold_property.action_sold()
        sold_property_offer = self._create_offer(
            sold_property,
            validity=-1,
        )

        processed_count = self.Offer._cron_refuse_expired_offers()

        self.assertEqual(processed_count, 1)
        self.assertEqual(expired_offer.status, "refused")
        self.assertEqual(current_offer.status, "pending")
        self.assertEqual(accepted_offer.status, "accepted")
        self.assertEqual(sold_property_offer.status, "pending")
        self.assertLess(expired_offer.date_deadline, fields.Date.today())
