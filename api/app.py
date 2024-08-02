from .constants import APP_HOST, APP_PORT, DEBUG_MODE
from .utils import *
from datetime import timedelta

from .routes.blog import blogBlueprint
from .routes.contact import contactBlueprint
from .routes.single_blog import single_blogBlueprint
from .routes.verifyUser import verifyUserBlueprint
from .routes.add import addBlueprint
from .routes.edit import editBlueprint

from .factory import create_app

app = create_app()
app.register_blueprint(blogBlueprint)
app.register_blueprint(contactBlueprint)
app.register_blueprint(verifyUserBlueprint)
app.register_blueprint(single_blogBlueprint)
app.register_blueprint(addBlueprint)
app.register_blueprint(editBlueprint)

dbFolder()
usersTable()
postsTable()
commentsTable()

# match __name__:
#     case "__main__":
startTime = currentTimeStamp()
Log.app(f"Running on http://{APP_HOST}:{APP_PORT}")
Log.success("App started")
app.run(debug=DEBUG_MODE, host=APP_HOST, port=APP_PORT)
endTime = currentTimeStamp()
runTime = endTime - startTime
runTime = str(timedelta(seconds=runTime))
Log.app(f"Run time: {runTime} ")
Log.app("Shut down")
Log.warning("App shut down")
Log.breaker()

