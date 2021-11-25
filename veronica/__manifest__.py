# Copyright 2021 Akretion (https://www.akretion.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Veronica",
    "summary": "Veronica Open API integration",
    "version": "14.0.1.0.1",
    "category": "Accounting & Finance",
    "website": "accioma.com",
    "author": "Accioma",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "l10n_ec_edi",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/veronica_views.xml",
        "data/settings_data.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
