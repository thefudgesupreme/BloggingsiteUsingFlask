from FlaskBlog import createApp

app=createApp()

if __name__=='__main__':
    app.run(debug=True, host = '0.0.0.0')
    # , host = '0.0.0.0'
    #host=192.168.43.107
