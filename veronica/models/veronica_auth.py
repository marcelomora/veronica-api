# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import requests, json
from datetime import timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

        
class VeronicaAuth(models.Model):
    _name = 'veronica.auth'
    _rec_name = 'username'
    _description = 'Veronica Auth'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        readonly=True,
        states={
                'draft': [('readonly', False)],
                'refused': [('readonly', False)]},
            default=lambda self: self.env.company)

    

    username = fields.Char("Username")
    active = fields.Boolean("Active", default=True)
    password = fields.Char("Password")
    client_id = fields.Char("Client ID")
    client_secret = fields.Char("Client Secret")
    token_from = fields.Datetime("Token From")
    token_to = fields.Datetime("Token To")
    access_token = fields.Char("Access Token")
    refresh_token = fields.Char("Refresh Token")


        
    def get_token(self):
        self.ensure_one()
        url = self.env['veronica.url_mgr'].get_token_url()

        payload={'username': self.username,
                 'password': self.password,}
        
        response = requests.post(url, data=payload, verify=False,
                                 allow_redirects=False,
                                 auth=(self.client_id, self.client_secret))

        if response.status_code != 200:
            raise UserError(_("Failed to obtain token from Veronica server {}").format(response.status_code))

        response_json = response.json()

        self.access_token = response_json["access_token"]
        self.refresh_token = response_json["refresh_token"]
        self.token_to = fields.Datetime.now() + timedelta(seconds = int(response_json["expires_in"]) - 5)
        self.token_from = fields.Datetime.now()

    def get_access_token(self):
        self.ensure_one()

        now = fields.Datetime.now()
        _logger.info("now {}, afer {}".format(now, self.token_from + timedelta(minutes = 2)))
        if self.token_from + timedelta(minutes = 2) > now:
            return self.access_token

        self.get_token()
        return self.access_token





