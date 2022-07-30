
def equity_monthly_amount_clean(request_post):
    return {
        'increases_january': request_post.get('increases_january').replace(',', ''),
        'increases_february': request_post.get('increases_february').replace(',', ''),
        'increases_march': request_post.get('increases_march').replace(',', ''),
        'increases_april': request_post.get('increases_april').replace(',', ''),
        'increases_may': request_post.get('increases_may').replace(',', ''),
        'increases_june': request_post.get('increases_june').replace(',', ''),
        'increases_july': request_post.get('increases_july').replace(',', ''),
        'increases_august': request_post.get('increases_august').replace(',', ''),
        'increases_september': request_post.get('increases_september').replace(',', ''),
        'increases_october': request_post.get('increases_october').replace(',', ''),
        'increases_november': request_post.get('increases_november').replace(',', ''),
        'increases_december': request_post.get('increases_december').replace(',', '')
    }
