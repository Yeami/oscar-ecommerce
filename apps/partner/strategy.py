from oscar.apps.partner.models import Partner
from oscar.apps.partner.strategy import Default as CoreDefault


class Selector(object):
    def strategy(self, request=None, user=None, **kwargs):
        return Default(request)


class Default(CoreDefault):
    """
    Partner strategy, that returns prices from stockrecord
    depending on user partner group
    """
    product = None
    partners = None

    def select_stockrecord(self, product):
        self.product = product
        try:
            return self.get_product_for_auth_user() if self.user else self.get_default_product()
        except IndexError:
            return None

    def get_product_for_auth_user(self):
        self.partners = Partner.objects.filter(users=self.user.id)

        return self.get_product_for_partner() if len(self.partners) else self.get_default_product()

    def get_product_for_partner(self):
        for partner in self.partners:
            product = self.get_partner_product(partner)

            if len(product):
                return product[0]

        return self.get_default_product()

    def get_partner_product(self, partner):
        return self.product.stockrecords.filter(partner=partner)

    def get_default_product(self):
        partner = Partner.objects.filter(code='default')[0]

        return self.product.stockrecords.filter(partner=partner)[0]
