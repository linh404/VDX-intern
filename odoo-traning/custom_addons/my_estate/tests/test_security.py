from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged, new_test_user


@tagged("post_install", "-at_install")
class TestEstateSecurity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.estate_user = new_test_user(
            cls.env,
            login="estate_user_test",
            groups="my_estate.group_estate_user",
        )
        cls.other_estate_user = new_test_user(
            cls.env,
            login="other_estate_user_test",
            groups="my_estate.group_estate_user",
        )
        cls.estate_manager = new_test_user(
            cls.env,
            login="estate_manager_test",
            groups="my_estate.group_estate_manager",
        )

        cls.Property = cls.env["estate.property"]
        cls.Offer = cls.env["estate.property.offer"]

        cls.user_property = cls.Property.create({
            "name": "User property",
            "expected_price": 100000.0,
            "salesperson_id": cls.estate_user.id,
        })
        cls.unassigned_property = cls.Property.create({
            "name": "Unassigned property",
            "expected_price": 120000.0,
            "salesperson_id": False,
        })
        cls.other_user_property = cls.Property.create({
            "name": "Other user property",
            "expected_price": 140000.0,
            "salesperson_id": cls.other_estate_user.id,
        })
        cls.properties = (
            cls.user_property
            | cls.unassigned_property
            | cls.other_user_property
        )

        cls.partner = cls.env["res.partner"].create({"name": "Security Test Buyer"})
        cls.user_property_offer = cls.Offer.create({
            "property_id": cls.user_property.id,
            "partner_id": cls.partner.id,
            "price": 95000.0,
        })
        cls.unassigned_property_offer = cls.Offer.create({
            "property_id": cls.unassigned_property.id,
            "partner_id": cls.partner.id,
            "price": 115000.0,
        })
        cls.other_user_property_offer = cls.Offer.create({
            "property_id": cls.other_user_property.id,
            "partner_id": cls.partner.id,
            "price": 130000.0,
        })
        cls.offers = (
            cls.user_property_offer
            | cls.unassigned_property_offer
            | cls.other_user_property_offer
        )

    def test_estate_user_only_sees_own_or_unassigned_properties(self):
        visible_properties = self.Property.with_user(self.estate_user).search([
            ("id", "in", self.properties.ids),
        ])

        self.assertEqual(
            set(visible_properties.ids),
            {self.user_property.id, self.unassigned_property.id},
        )

    def test_estate_manager_sees_all_properties(self):
        visible_properties = self.Property.with_user(self.estate_manager).search([
            ("id", "in", self.properties.ids),
        ])

        self.assertEqual(set(visible_properties.ids), set(self.properties.ids))

    def test_estate_user_only_sees_offers_for_own_or_unassigned_properties(self):
        visible_offers = self.Offer.with_user(self.estate_user).search([
            ("id", "in", self.offers.ids),
        ])

        self.assertEqual(
            set(visible_offers.ids),
            {self.user_property_offer.id, self.unassigned_property_offer.id},
        )

    def test_estate_manager_sees_all_offers(self):
        visible_offers = self.Offer.with_user(self.estate_manager).search([
            ("id", "in", self.offers.ids),
        ])

        self.assertEqual(set(visible_offers.ids), set(self.offers.ids))

    def test_estate_user_cannot_unlink_properties(self):
        with self.assertRaises(AccessError):
            self.user_property.with_user(self.estate_user).unlink()

    def test_estate_manager_can_unlink_properties(self):
        property_to_unlink = self.Property.create({
            "name": "Manager unlink property",
            "expected_price": 160000.0,
            "salesperson_id": self.other_estate_user.id,
        })

        property_to_unlink.with_user(self.estate_manager).unlink()

        self.assertFalse(property_to_unlink.exists())

    def test_estate_user_cannot_manage_configuration_models(self):
        with self.assertRaises(AccessError):
            self.env["estate.property.type"].with_user(self.estate_user).create({
                "name": "Forbidden type",
            })

        with self.assertRaises(AccessError):
            self.env["estate.property.tag"].with_user(self.estate_user).create({
                "name": "Forbidden tag",
            })
