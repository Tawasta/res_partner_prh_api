# -*- coding: utf-8 -*-

# 1. Standard library imports:
import requests
import json

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResPartner(models.Model):
    
    # 1. Private attributes
    _inherit = 'res.partner'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.onchange('business_id')
    def onchange_business_id_update_info(self):
        if not self.business_id:
            return False

        url = 'http://avoindata.prh.fi/tr/v1/' + self.business_id
        response = requests.get(url)
        json_response = response.json()

        if not 'results' in json_response:
            return False

        if len(json_response['results']) == 0:
            return False

        results = json_response['results'][0]

        # Update name
        if not self.name:
            self.name = results['name']

        # Update address details
        if 'addresses' in results:
            # TODO: this can only handle the first address. Create affiliate companies from others

            address = results['addresses'][0]

            if not self.website:
                self.website = address['website']

            if not self.city:
                self.city = address['city']

            if not self.fax:
                self.fax = address['fax']

            if not self.country_id:
                self.country_id = self.env['res.country'].search([('code', '=', address['country'])], limit=1).id

            if not self.phone:
                self.phone = address['phone']

            if not self.street:
                self.street = address['street']

            if not self.zip:
                self.zip = address['postCode']

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
