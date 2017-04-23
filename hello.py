def app(env, start_response):
	data = env["QUERY_STRING"].split("&")
	output = [bytes(entry + '\n', 'ascii') for entry in data]
	status = '200 OK'
	headers = [
		('Content-Type', 'text/plain')
	]

	start_response(status, headers)
	return output
