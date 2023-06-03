"""
This WebApp is the interface for the tennis league checker python code
"""
import sys
print(sys.version)


from dash import Dash, dcc, html, dash_table, dependencies
import os

app = Dash()
server = app.server      #exposes server of dash app as an objective that gunicorn can pick
app.title = 'Tennis League Eligibility Cheker'  # set the title to appear in the tab


if __name__ == '__main__':
    #app.run_server()  # Set debug to true makes webapp automatically update, when user clicks refresh
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))