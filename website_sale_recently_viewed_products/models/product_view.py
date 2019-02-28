from openerp import api, fields, models, _


class ProductHistory(models.Model):
    _name = 'website.sale.product.view'
    _description = 'Ecommerce Product Views'

    sessionid = fields.Char('Session ID', index=True)
    product_id = fields.Many2one('product.template', 'Product')
    last_view_datetime = fields.Datetime(
        'Last view datetime', default=fields.Datetime.now)

    _sql_constraints = [
        ('unique_session_product', 'UNIQUE(sessionid, product_id)',
         'There is already a record for this product and session')
    ]
    _order = 'last_view_datetime DESC'

    @api.multi
    def human_readable_datetime_difference(self, now=None):
        """
        Return an human readable form of the difference between the supplied
        datetime (or the current datetime if not supplied) and the history
        record ``last_view_datetime``.
        """
        if now is None:
            now = fields.Datetime.from_string(fields.Datetime.now())
        timedifference = now - fields.Datetime.from_string(
            self.last_view_datetime)
        minutes = timedifference.seconds // 60
        hours = timedifference.seconds // 3600
        days = timedifference.days
        # string concatenation and explicit singular/plural
        # to make life easier for translators
        if days > 1:
            return _('%s days ago') % str(days)
        elif days == 1:
            return _('%s Yesterday') % str(days)
        elif hours > 1:
            return _('%s hours ago') % str(hours)
        elif hours == 1:
            return _('%s hour ago') % str(hours)
        elif minutes > 1:
            return _('%s minutes ago') % str(minutes)
        elif minutes == 1:
            return _('%s minute ago') % str(minutes)
        return _('Less than a minute ago')
