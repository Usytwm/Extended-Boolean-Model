from tools.process_dnf import (get_literals_from_dnf, query_to_dnf)




query_dnf = query_to_dnf(query)
print(query_dnf)

query_literals = get_literals_from_dnf(query_dnf)
print(query)

