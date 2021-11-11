# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import requests, base64, logging
from lxml import etree
#  import http.client as http_client
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

class EcWaybill(models.Model):
    _inherit = 'ec.waybill'

    def _post_waybill_edi(self):
        """Overrides"""

        for waybill in self:

            xml_raw = waybill.waybill_generate_xml()
            parser = etree.XMLParser(remove_blank_text=True)
            elem = etree.XML(xml_raw, parser=parser)
            data = etree.tostring(elem).decode("utf-8")

            ak = self.env['veronica.url_mgr'].send_data(waybill.company_id, data)

            if not ak:
                return False

            waybill.l10n_ec_waybill_access_key = ak
            return True

    def action_validate(self):
        _logger.info("Action Validate")
        super(EcWaybill, self).action_validate()
        post_waybill = self._post_waybill_edi()
        
        if post_waybill:
            self.write({'state': 'in-progress'})
