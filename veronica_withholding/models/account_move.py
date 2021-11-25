# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import requests, base64, logging
from lxml import etree
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        """Send withholdig to Veronica on post action"""
        super(AccountMove, self).action_post()
        for move in self:
            if move.move_type != "in_invoice" \
                    and move.l10n_ec_withholding_type != "out_withholding":
                continue

            # Calculate withholdig number from l10n_ec_withholding
            #  super(AccountMove, self)._compute_name()

            xml_raw = move._export_withhold_as_xml()
            parser = etree.XMLParser(remove_blank_text=True)
            elem = etree.XML(xml_raw, parser=parser)
            data = etree.tostring(elem).decode("utf-8")

            response = self.env['veronica.url_mgr'].send_data(move.company_id, data)

            if response.get('success', False):
                move.l10n_ec_withholding_access_key = response.get('result').get('claveAcceso') or \
                    response.get('result').get('claveAccesoConsultada')

            if response.get('success', False) == False:
                defalut_msg = _("Veronica was not returned any access key. Please contact technical support")
                result = response.get('result', False)
                if result:
                    msg = result.get('message', defalut_msg)

                    move.message_post(body= "Veronica: " + msg)

