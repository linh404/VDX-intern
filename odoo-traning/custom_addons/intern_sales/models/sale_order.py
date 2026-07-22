from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


DISCOUNT_APPROVAL_THRESHOLD = 10.0


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(
        selection_add=[("to_approve", "To Approve")],
        ondelete={"to_approve": "set default"},
    )
    requires_approval = fields.Boolean(
        string="Requires Discount Approval",
        compute="_compute_requires_approval",
        store=True,
        readonly=True,
        help="Enabled when at least one order line has a discount above 10%.",
    )
    discount_approved = fields.Boolean(
        string="Discount Approved",
        readonly=True,
        copy=False,
    )
    discount_approved_by = fields.Many2one(
        comodel_name="res.users",
        string="Approved By",
        readonly=True,
        copy=False,
    )

    @api.depends("order_line.discount", "order_line.display_type")
    def _compute_requires_approval(self):
        for order in self:
            order.requires_approval = any(
                not line.display_type
                and line.discount > DISCOUNT_APPROVAL_THRESHOLD
                for line in order.order_line
            )

    def action_confirm(self):
        orders_to_approve = self.filtered(
            lambda order: order.requires_approval and not order.discount_approved
        )
        if orders_to_approve:
            orders_to_approve.filtered(lambda order: order.state in ("draft", "sent")).write({
                "state": "to_approve",
            })
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": self.env._("Discount approval required"),
                    "message": self.env._(
                        "Orders with a line discount above %(threshold).0f%% "
                        "must be approved before confirmation.",
                        threshold=DISCOUNT_APPROVAL_THRESHOLD,
                    ),
                    "type": "warning",
                    "sticky": False,
                },
            }
        res = super().action_confirm()
        if len(self) == 1 and self.picking_ids:
            return self.action_view_delivery()
        return res

    def action_approve_discount(self):
        self._check_discount_approver()
        for order in self:
            if order.state != "to_approve":
                raise UserError(
                    self.env._("Only orders waiting for discount approval can be approved.")
                )
            if not order.requires_approval:
                raise UserError(self.env._("This order does not require discount approval."))
            order.write({
                "discount_approved": True,
                "discount_approved_by": self.env.user.id,
                "state": "draft",
            })
            order.message_post(
                body=self.env._(
                    "Discount approved by %(user)s.",
                    user=self.env.user.display_name,
                )
            )
        return True

    def _check_discount_approver(self):
        if not self.env.user.has_group("intern_sales.group_discount_approver"):
            raise UserError(self.env._("Only Discount Approvers can approve discounts."))

    def _reset_discount_approval(self):
        orders_to_reset = self.filtered(lambda order: order.discount_approved)
        if orders_to_reset:
            orders_to_reset.write({
                "discount_approved": False,
                "discount_approved_by": False,
            })

    def _confirmation_error_message(self):
        self.ensure_one()
        if self.state == "to_approve":
            return self.env._("This order is waiting for discount approval.")
        error_msg = super()._confirmation_error_message()
        return error_msg


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.constrains("discount")
    def _check_discount(self):
        for line in self:
            if line.discount < 0.0 or line.discount > 100.0:
                raise ValidationError(self.env._("Discount must be between 0 and 100."))

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines.filtered(lambda line: line.discount)._reset_order_discount_approval()
        return lines

    def write(self, vals):
        orders = self.order_id if "discount" in vals else self.env["sale.order"]
        result = super().write(vals)
        orders._reset_discount_approval()
        return result

    def unlink(self):
        orders = self.order_id
        result = super().unlink()
        orders._reset_discount_approval()
        return result

    def _reset_order_discount_approval(self):
        self.order_id._reset_discount_approval()
