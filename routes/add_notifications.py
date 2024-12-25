
@app.route('/')
def home():
    return "welcome to the custom notification services!"

@app.route('/add_test_notifications')
def add_test_notification():
    new_notification = Notification(recipient="gabeamazing21@gmail.com", message="Hello, this is a test")
    db.session.add(new_notification)
    db.session.commit()
    return "Test notification added!"