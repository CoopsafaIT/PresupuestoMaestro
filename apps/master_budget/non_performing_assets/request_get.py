

class QueryGetParms():
    def __init__(self, data):
        self.page = data.get('page', 1)
        self.parameter = data.get('parameter')
        self.status = data.get('status')

    def get_query_filters(self):
        return {
            **({'parameter_id': self.parameter} if self.parameter else {}),
            **({'is_active': self.status} if self.status else {})
        }

    def get_page(self):
        return self.page
