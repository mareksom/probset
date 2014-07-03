def messages(request):
	error_mess = request.session.get('error',[])
	request.session['error'] = []
	success_mess = request.session.get('success',[])
	request.session['success'] = []
	return {'error_messages': error_mess, 'success_messages': success_mess}

from forum.utils import count_new_forum_threads

def forum_posts(request):
	return {'forum_new_threads' : count_new_forum_threads(request.user)}

from problems.utils import count_new_comments

def comments_posts(request):
	return {'comments_new_posts' : count_new_comments(request.user)}
