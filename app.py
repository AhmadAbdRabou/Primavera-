#'app.py'

# Primavera++
# This application tries to make the best of Programming, Statistics, Data Science, and Machine Learning in favor to Construction Project Planning
# In this cycle the application will focus on the Read-Only utilization of Primavera schema
# This application contains 5 separated Single Page Application (SPA)
#       /ProjectData: Responsible of handling XER files into workable Excel-books
#       /PrimaveraObjects: Responsible of exploring Primavera and provide some useful tools and views
#       /SpecializedReports: Responsible of creating a Decision-Making reports
#       /StatisticalReports: Responsible of the statistical reports
#       /Predictions: Responsible of Machine Learning predictions
# app.py is the main of Primavera++ application
# Instead of launching multiple applications using the command line 'app.py' launch the server programatically
# The reason for this is that debugging is not available when using command line luanch
# The main function is to create a server object (Bokeh Server) and initiate it with Bokeh Applications, port number, and any additional path to serve
# Bokeh Application is created using Bokeh FunctionHandler which is the function that handle the application page
# Addtional pathes are pathes for static files like css, js, or anything else which is presented to the server using 'extra_patterns' argument
# 'extra_pattern' maps between application path and on server path and requires a Tornado StaticFileHandler
# Tornado is the actual server which Bokeh Server utilizes 
# Tornado IOLoop acts a listener
# While in debugging mode and changes are invitable to happen, Tornado AutoReload is required to reload the static files like css

# Loading built-in packages
import sys
from os.path import dirname, join
# Loading Tornado packages
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler
import tornado.autoreload
# Loading Bokeh packages
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
# Loading application modules
from models import ProjectData
from models.Empty import modify_page2


# Create Bokeh Application using Bokeh FunctionHandler which calls project_data_loading function from ProjectDataLoading module
project_data = Application(FunctionHandler(ProjectData.init))
# Empty page
page2_app = Application(FunctionHandler(modify_page2))
# Create Tronado Main Event Loop
io_loop = IOLoop.current()
# Make Tornado watch the static file css while in development mode
tornado.autoreload.watch(join(dirname(__file__),"static","css","ProjectData.css"))
# start the watch and assign watch cycle
tornado.autoreload.start(check_time=500)
# The core function of the application, identifing the pathes to serve, the application for each path, the static files to serve, and port number
server = Server(applications = {'/ProjectData': project_data,
                                '/PrimaveraObjects': page2_app,
                                '/SpecializedReports': page2_app,
                                '/StatisticalReports': page2_app,
                                '/Predictions': page2_app},
                                # '/static/css' is used by the link for style sheet in the head section of related html template 
                                extra_patterns=[(r'/static/css/(.*)', StaticFileHandler, {'path':join(dirname(__file__),"static","css")}),
                                # '/static/js' is used by html template to render Bokeh objects 
                                (r'/static/js/(.*)', StaticFileHandler, {'path':join(dirname(__file__),"static","js")}),
                                # '/data/extracted_projects/' is used to provide link for downloading files in latter stage of the application
                                (r'/data/extracted_projects/(.*)', StaticFileHandler, {'path':join(dirname(__file__),"data","extracted_projects")})],
                                io_loop = io_loop, port = 5006)
# Starting server
server.start()
# Launch the default browser and load the selected page
server.show('/ProjectData')
# Start listening
io_loop.start() 

