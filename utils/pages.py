from math import ceil

def compute_pages(page, count, per_page = 10):
	last_page = max(1, ceil(count/per_page))
	page = max(1,min(last_page, int(page)))

	visible = list(set([1, last_page] + [i for i in range(page-2, page+3) if i>1 and i < last_page]))
	visible.sort()
	ready_list = [1]
	for i in range(1, len(visible)):
		if visible[i]-1 != ready_list[-1]:
			ready_list.append('...')
		ready_list.append(visible[i])
	
	for i in range(1, len(ready_list)-1):
		if ready_list[i] == '...' and ready_list[i-1]+2 == ready_list[i+1]:
			ready_list[i] = ready_list[i-1]+1
		
	context = {'page' : page,
		'pages' : ready_list,
		'last_page' : last_page,
		'next_page' : page+1,
		'prev_page' : page-1}
	return context
