# Copyright 2021 Akretion (https://www.akretion.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import requests, base64, logging
from lxml import etree
#  import http.client as http_client
from odoo import _, api, fields, models


#  logging.basicConfig()
#  logging.getLogger().setLevel(logging.DEBUG)
#  requests_log = logging.getLogger("requests.packages.urllib3")
#  requests_log.setLevel(logging.DEBUG)
#  requests_log.propagate = True
#
_logger = logging.getLogger(__name__)

class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    def _post_invoice_edi(self, invoices, test_mode=False):
        """Overrides"""

        url = "{}{}".format(
            self.env['ir.config_parameter'].sudo().get_param("veronica.base.url"),
            self.env['ir.config_parameter'].sudo().get_param("veronica.comprobantes.url"))

        result = super(AccountEdiFormat, self)._post_invoice_edi(invoices, test_mode = test_mode)

        for move, values in result.items():
            auth = self.env['veronica.auth'].search(
                [('company_id', '=', move.company_id.id)]
            )[0]

            token = auth.get_access_token()
            _logger.info(token)
            _logger.info(url)

            _logger.info("result {}, values {}".format(move, values))
            xml_raw = values["attachment"].raw  #.decode("utf-8")
            parser = etree.XMLParser(remove_blank_text=True)
            elem = etree.XML(xml_raw, parser=parser)
            data = etree.tostring(elem).decode("utf-8")

            #  data = {'xml': xml}
            _logger.info(data)
            headers = {
                "Authorization": "Bearer {}".format(token),
                'Content-Type': 'application/atom+xml'
            }

            response = requests.post(url, data=data, headers=headers)
            _logger.info("Veronica response {}".format(response.json()))
        return result






    

