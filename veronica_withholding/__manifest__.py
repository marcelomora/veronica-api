# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Veronica Withholding",
    "summary": "Send withholds to Veronica so it can be authorized by SRI",
    "version": " 14.0.1.0.2",
    "category": "Accounting & Finance",
    "website": "accioma.com",
    "author": "Marcelo Mora (marcelo.mora@accioma.com)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "veronica", "l10n_ec_withholding",
    ],
    "data": [
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
