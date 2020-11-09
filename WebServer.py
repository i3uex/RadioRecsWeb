import json
import logging
import uuid
import os.path

import cherrypy
from predictor import RecommendationSystem


class WebServer(object):
    @cherrypy.expose
    def index(self):
        """
        Creates a new session id
        Serves the home page
        """
        session_id = str(uuid.uuid4())
        cherrypy.session["id"] = session_id

        return open('static/index.html', encoding='utf-8')


@cherrypy.expose
class MakePredictionService(object):
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, data):
        """
        Serves the data needed to render the home page
        """
        logging.debug(f"MakePredictionService.POST()")

        try:
            options = json.loads(data)

            voice_percentage = options["voicePercentage"]
            music_genres = options["musicGenres"]
            analytical_percentage = options["analyticalPercentage"]
            anger_percentage = options["angerPercentage"]
            confident_percentage = options["confidentPercentage"]
            fear_percentage = options["fearPercentage"]
            joy_percentage = options["joyPercentage"]
            sadness_percentage = options["sadnessPercentage"]
            tentative_percentage = options["tentativePercentage"]
            topics = options["topics"]
            programs = options["programs"]

            result = RecommendationSystem.predict(
                voice_percentage,
                music_genres,
                analytical_percentage,
                anger_percentage,
                confident_percentage,
                fear_percentage,
                joy_percentage,
                sadness_percentage,
                tentative_percentage,
                topics,
                programs
            )
        except Exception as exception:
            message = f"{str(exception)}"
            logging.error(message)
            raise cherrypy.HTTPError(500, message=message)

        return result


@cherrypy.expose
class SaveFeedbackService(object):
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, data):
        """
        Serves the data needed to render the home page
        """
        logging.debug(f"SaveFeedbackService.POST("
                      f"data={data})")

        try:
            options = json.loads(data)
            feedback = options["feedback"]
            ip = cherrypy.request.remote.ip
            user_agent = cherrypy.request.headers["User-Agent"]

            file_name = "feedback.csv"
            if not os.path.isfile(file_name):
                file = open("feedback.csv", "a")
                file.write("feedback,ip,user_agent\n")
                file.close()

            file = open("feedback.csv", "a")
            file.write(f"{feedback},{ip},{user_agent}\n")
            file.close()
        except Exception as exception:
            message = f"{str(exception)}"
            logging.error(message)
            raise cherrypy.HTTPError(500, message=message)
