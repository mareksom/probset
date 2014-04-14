def error_msg(request,error):
	request.session['error'] = request.session.get('error',[]) + [error]

def success_msg(request,success):
	request.session['success'] = request.session.get('success',[]) + [success]
