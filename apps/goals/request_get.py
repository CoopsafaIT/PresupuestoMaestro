class QueryGetParms():
    def __init__(self, data):
        self.code_zone = data.getlist('code_zone')

    def get_query_filters(self):
        return {
            **({'id_cost_center__code_zone__in': self.code_zone} if self.code_zone else {}), # NOQA
        }

    def get_page(self):
        return self.page
