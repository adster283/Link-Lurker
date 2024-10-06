import whois
from datetime import datetime

def get_time_dif(date_to_check):
    current_date = datetime.now()

    # Handle case where date_to_check could be a list
    if isinstance(date_to_check, list):
        date_to_check = date_to_check[0]

    # Ensure date_to_check is not None
    if date_to_check is None:
        return None

    days = (current_date - date_to_check).days
    return days

def check_dns_records(url):
    private_info = False
    days_since_creation = None
    days_since_edit = None
    days_till_expiration = None

    try:
        results = whois.whois(url)

        # Check if data is redacted
        if 'REDACT' in str(results.get('org', '')):
            private_info = True
        
        # Check if domain was created or edited recently
        days_since_creation = get_time_dif(results.get('creation_date', None))
        days_since_edit = get_time_dif(results.get('updated_date', None))
        days_till_expiration = get_time_dif(results.get('expiration_date', None))

        # TODO: registrar, country, status, nameservers

        return {'private_info' : private_info,
                'days_since_creation' : days_since_creation,
                'days_since_edit' : days_since_edit,
                'days_till_expiration' : days_till_expiration}

    except Exception as e:
        print(f"Error retrieving WHOIS information: {e}")

if __name__ == "__main__":

    # Simple test function call to see what we return
    print(check_dns_records("cloudflare.com"))
