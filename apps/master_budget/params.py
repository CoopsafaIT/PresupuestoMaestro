class QueryGetParms():
    def __init__(self, data):
        self.page = data.get('page', 1)
        self.period_id = data.get('period_id')
        self.status = data.get('status')

    def get_query_filters(self):
        return {
            **({'period_id': self.period_id} if self.period_id else {}),
            **({'is_active': self.status} if self.status else {})
        }

    def get_page(self):
        return self.page
