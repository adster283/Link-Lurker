from fuzzywuzzy import fuzz

def check_match(bad_domains, threshold=80):
    good_domains = ['microsoft.com', 'nzpost.com', 'aupost.com', 'facebook.com', 'cloudflare.com']
    domains_found = []

    for bad_domain in bad_domains:
        for good_domain in good_domains:
            similarity = fuzz.ratio(bad_domain, good_domain)
            if threshold < similarity < 100:
                print(f'We have a likely scam or phishing attempt: {bad_domain} (similar to {good_domain})')
                domains_found.append(bad_domain)
    
    if len(domains_found) > 0:
        return {'result': True, 'domains': domains_found}
    else:
        return {'result': False, 'domains': domains_found}

def check_chars(domain):
    allowed_characters = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._+@')
    disallowed_chars = [char for char in domain if char not in allowed_characters]
    
    return disallowed_chars if disallowed_chars else None

if __name__ == '__main__':
    # Example test
    test_list = ['cl0udflare.com']
    check_match(test_list)
    pass
