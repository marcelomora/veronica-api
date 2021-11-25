# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import requests, base64
  
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

class VeronicaUrl_Mgr(models.TransientModel):
    _name = 'veronica.url_mgr'
    _description = 'Veronica URL Manager'


    def get_url(self):
        """Returns the Veronica URL that matches config"""

        is_one_step = self.env['ir.config_parameter'].sudo().get_param('veronica.sri')
        env = self.env['ir.config_parameter'].sudo().get_param('l10n_ec_edi.environment_type')
        base_url = self.env['ir.config_parameter'].sudo().get_param("veronica.base.test.url")

        if env == '2':
            base_url = self.env['ir.config_parameter'].sudo().get_param("veronica.base.prod.url")

        if is_one_step:
            send_url = self.env['ir.config_parameter'].sudo().get_param("veronica.sri.url")
        else:
            send_url = self.env['ir.config_parameter'].sudo().get_param("veronica.comprobantes.url")

        return "{}{}".format(
            base_url, send_url)
    
    def get_token_url(self):
        """Returns the Veronica URL that matches config"""

        env = self.env['ir.config_parameter'].sudo().get_param('l10n_ec_edi.environment_type')
        base_url = self.env['ir.config_parameter'].sudo().get_param("veronica.base.test.url")

        if env == '2':
            base_url = self.env['ir.config_parameter'].sudo().get_param("veronica.base.prod.url")

        auth_url = self.env['ir.config_parameter'].sudo().get_param("veronica.auth.url")

        _logger.info("{}{}".format(base_url, auth_url))

        return "{}{}".format(
            base_url, auth_url)

    def send_data(self, company_id, data):
        """Send data to Veronica"""

        url = self.get_url()
        auth = self.env['veronica.auth'].search(
            [('company_id', '=', company_id.id)]
        )[0]
        token = auth.get_access_token()

        _logger.info(data)
        _logger.info(token)

        headers = {
            "Authorization": "Bearer {}".format(token),
            'Content-Type': 'application/atom+xml'
        }

        response = requests.post(url, data=data, headers=headers)
        vero_response = response.json()
        _logger.info("Veronica response {}".format(vero_response))

        return vero_response

        #  if vero_response.get('success', False):
        #      return \
        #          vero_response.get('result').get('claveAcceso') or \
        #          vero_response.get('result').get('claveAccesoConsultada')
        #  else:
        #      return vero_response.get('result')
        #
        #
        #  return False
