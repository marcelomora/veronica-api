# Copyright 2021 Accioma (https://www.akretion.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    veronica_url = fields.Char("Veronica URL", config_parameter="veronica.url")
    veronica_sri = fields.Boolean("Veronica One Step", config_parameter="veronica.sri")
    

