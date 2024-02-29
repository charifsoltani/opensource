# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>

{
    'name': 'wkhtmltopdf Large PDF',
    'version': '16.0.1',
    "author": "Charif SOLTANI",
    "website": "https://www.linkedin.com/in/soltani-charif-b0351811a/",
    'category': 'Base',
    'description': """
       This app enables you to print a substantial number of documents simultaneously, eliminating the occurrence of the code: -11 error associated with wkhtmltopdf.
       If you continue to encounter this error, you may need to adjust the "base.wkhtmltopdf_max_files" parameter in the system settings to a lower value.
    """,
    "license": "AGPL-3",
    'depends': ['base'],
    'data': ['data/ir_config_data.xml'],
    'qweb': [],
    'demo': [],
    'test': [],
    'application': False,
    'installable': True,
    'auto_install': False,
}
