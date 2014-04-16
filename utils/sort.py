# sortowanie uwzględniające polskie znaki

lista = (('ą','aą'), ('ć', 'cć'), ('ę', 'eę'), ('ł', 'lł'), ('ń', 'nń'), ('ó', 'oó'), ('ś', 'sś'), ('ź', 'zź'), ('ż', 'zż'),
					('a','aa'), ('c', 'cc'), ('e', 'ee'), ('l', 'll'), ('n', 'nn'), ('o', 'oo'), ('s', 'ss'), ('z', 'zz'))
slownik = {}
for i in lista:
	slownik[i[0]] = i[1]

def pl_filter(s):
	news = ''
	for c in s:
		news += slownik.get(c,c)
	return news
