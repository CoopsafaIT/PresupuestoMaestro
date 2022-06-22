from decimal import Decimal as dc

def others_assets_monthly_amount_clean(request_post):
    return {
        'amount_january': request_post.get('amount_january').replace(',', ''),
        'amount_february': request_post.get('amount_february').replace(',', ''),
        'amount_march': request_post.get('amount_march').replace(',', ''),
        'amount_april': request_post.get('amount_april').replace(',', ''),
        'amount_may': request_post.get('amount_may').replace(',', ''),
        'amount_june': request_post.get('amount_june').replace(',', ''),
        'amount_july': request_post.get('amount_july').replace(',', ''),
        'amount_august': request_post.get('amount_august').replace(',', ''),
        'amount_september': request_post.get('amount_september').replace(',', ''),
        'amount_october': request_post.get('amount_october').replace(',', ''),
        'amount_november': request_post.get('amount_november').replace(',', ''),
        'amount_december': request_post.get('amount_december').replace(',', '')
    }


def others_assets_monthly_percentage_clean(request_post):
    return {
        'percentage_january': dc(request_post.get('percentage_january')) / 100,
        'percentage_february': dc(request_post.get('percentage_february')) / 100,
        'percentage_march': dc(request_post.get('percentage_march')) / 100,
        'percentage_april': dc(request_post.get('percentage_april')) / 100,
        'percentage_may': dc(request_post.get('percentage_may')) / 100,
        'percentage_june': dc(request_post.get('percentage_june')) / 100,
        'percentage_july': dc(request_post.get('percentage_july')) / 100,
        'percentage_august': dc(request_post.get('percentage_august')) / 100,
        'percentage_september': dc(request_post.get('percentage_september')) / 100,
        'percentage_october': dc(request_post.get('percentage_october')) / 100,
        'percentage_november': dc(request_post.get('percentage_november')) / 100,
        'percentage_december': dc(request_post.get('percentage_december')) / 100
    }
