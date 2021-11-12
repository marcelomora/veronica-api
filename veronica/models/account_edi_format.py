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

        result = super(AccountEdiFormat, self)._post_invoice_edi(invoices, test_mode = test_mode)

        for move, values in result.items():

            _logger.info("result {}, values {}".format(move, values))
            xml_raw = values["attachment"].raw  #.decode("utf-8")
            parser = etree.XMLParser(remove_blank_text=True)
            elem = etree.XML(xml_raw, parser=parser)
            data = etree.tostring(elem).decode("utf-8")

            #  data = {'xml': xml}
            _logger.info(data)
            ak = self.env['veronica.url_mgr'].send_data(move.company_id, data)
            l10n_ec_move_access_key = ak
        return result






    

