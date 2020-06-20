from oscar.apps.partner.strategy import Default as CoreDefault


class Selector(object):
    def strategy(self, request=None, user=None, **kwargs):
        return Default(request)


class Default(CoreDefault):
    """
    Partner strategy, that returns prices from stockrecord
    depending on user partner group
    """

    def select_stockrecord(self, product):
        try:
            from oscar.apps.partner.models import Partner

            if self.user:
                partner = Partner.objects.filter(users=self.user.id)[0]
            else:
                partner = Partner.objects.filter(code='default')[0]

            return product.stockrecords.filter(partner=partner)[0]
        except IndexError:
            return None
