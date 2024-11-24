import dns.resolver

def get_dns_records(domain):
    record_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'SOA', 'SRV', 'PTR']
    results = {}

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            results[record_type] = [str(rdata) for rdata in answers]
        # except dns.resolver.NoAnswer:
        #     results[record_type] = "No records found"
        # except dns.resolver.NXDOMAIN:
        #     results[record_type] = "Domain does not exist"
        #     break
        except Exception as e:
            print("Error: ", e)

    return results

if __name__ == "__main__":
    
    # A test case
    domain = "m1crosoft.com"
    dns_records = get_dns_records(domain)
    for record_type, records in dns_records.items():
        print(f"{record_type} Records: {records}")
