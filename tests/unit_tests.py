from COVIDMonitor.main import app

# def test_monitor():
# 	response = app.test_client().get('/monitor')
#
# 	assert response.status_code == 200
# 	assert response.data == b'Welcome to the Covid Monitor!'

def test_upload():
	response = app.test_client().get('/upload')
	assert response.status_code == 200

def test_search():
	response = app.test_client().get('/search')

	assert response.status_code == 200

