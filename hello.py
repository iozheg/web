def app(env, start_response):
	data = env["QUERY_STRING"].split("&")
	status = '200 OK'
	headers = [
		('Content-Type', 'text/plain')
	]

	start_response(status, headers)
	return data
