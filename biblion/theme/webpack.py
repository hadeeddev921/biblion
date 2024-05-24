# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""JS/CSS bundles for rero-ils-ui.

You include one of the bundles in a page like the example below (using
``base`` bundle as an example):
.. code-block:: html
    {{ webpack['base.js']}}
"""

from flask_webpackext import WebpackBundle

theme = WebpackBundle(
    __name__,
    "assets",
    entry={
        "global": "./scss/biblion/styles.scss",
        "biblion_public": "./js/biblion/public.js",
        "babeltheque": "./scss/biblion/babeltheque.scss",
    },
    dependencies={
        "popper.js": "1.16.1",
        "jquery": "^3.7",
        "bootstrap": "~4.5.3",
        "@fortawesome/fontawesome-free": "^7.0.0",
    },
)
