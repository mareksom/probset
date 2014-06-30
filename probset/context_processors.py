from kasia.kasia import am_kasia, KASIA_USERNAME

def messages(request):
	error_mess = request.session.get('error',[])
	request.session['error'] = []
	success_mess = request.session.get('success',[])
	request.session['success'] = []
	return {'error_messages': error_mess, 'success_messages': success_mess}

def kasia(request):
	return {'is_kasia' : am_kasia(request), 'kasia_username' : KASIA_USERNAME}
