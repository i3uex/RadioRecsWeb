import logging

import cherrypy
import requests


class RecommendationSystem(object):
    @staticmethod
    def predict(
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
    ):
        logging.debug(f"RecommendationSystem.predict("
                      f"voice_percentage={voice_percentage}, "
                      f"music_genres={music_genres}, "
                      f"analytical_percentage={analytical_percentage}, "
                      f"anger_percentage={anger_percentage}, "
                      f"confident_percentage={confident_percentage}, "
                      f"fear_percentage={fear_percentage}, "
                      f"joy_percentage={joy_percentage}, "
                      f"sadness_percentage={sadness_percentage}, "
                      f"tentative_percentage={tentative_percentage}, "
                      f"topics={topics}, "
                      f"programs={programs})")

        try:
            RecommendationSystem.rs1a(
                voice_percentage
            )
            RecommendationSystem.rs2a(
                music_genres
            )
            RecommendationSystem.rs3a(
                topics
            )
            RecommendationSystem.rs4a(
                analytical_percentage,
                anger_percentage,
                confident_percentage,
                fear_percentage,
                joy_percentage,
                sadness_percentage,
                tentative_percentage
            )
        except Exception as exception:
            message = f"{str(exception)}"
            raise cherrypy.HTTPError(500, message=message)

        return "yeah"

    @staticmethod
    def rs1a(voice_percentage):
        logging.debug(f"RecommendationSystem.rs1a("
                      f"voice_percentage={voice_percentage})")

        try:
            music_percentage = 100 - int(voice_percentage)
            logging.debug(f"- music_percentage: {music_percentage}")
            url = f"http://localhost:9090/rs1a?voice={voice_percentage}&music={music_percentage}"
            logging.debug(f"- url: {url}")
            response = requests.get(url)
            logging.debug(f"- response.status_code: {response.status_code}")
        except Exception as exception:
            message = f"{str(exception)}"
            raise cherrypy.HTTPError(500, message=message)

        return response

    @staticmethod
    def rs2a(music_genres):
        logging.debug(f"RecommendationSystem.rs2a("
                      f"music_genres={music_genres})")

        try:
            music_genres_list = music_genres[0].split(",")
            music_genres_argument = ""
            for music_genre in music_genres_list:
                logging.debug(f"- music_genre: {music_genre}")
                music_genres_argument += f"{music_genre}=1&"
            if music_genres_argument != "":
                music_genres_argument = music_genres_argument[:-1]
            logging.debug(f"- music_genres_argument: {music_genres_argument}")
            url = f"http://localhost:9090/rs2a?{music_genres_argument}"
            logging.debug(f"- url: {url}")
            response = requests.get(url)
            logging.debug(f"- response.status_code: {response.status_code}")
        except Exception as exception:
            message = f"{str(exception)}"
            raise cherrypy.HTTPError(500, message=message)

        return response

    @staticmethod
    def rs3a(topics):
        logging.debug(f"RecommendationSystem.rs3a("
                      f"topics={topics})")

        try:
            topics_list = topics[0].split(",")
            topics_arguments = ""
            if "informativo" in topics_list:
                topics_arguments += "news=1&"
            else:
                topics_arguments += "news=0&"

            if "deportes" in topics_list:
                topics_arguments += "sport=1&"
            else:
                topics_arguments += "sport=0&"

            if "entretenimiento" in topics_list:
                topics_arguments += "entertainment=1&"
            else:
                topics_arguments += "entertainment=0&"

            if "musical" in topics_list:
                topics_arguments += "musical=1&"
            else:
                topics_arguments += "musical=0&"

            if "educacion" in topics_list:
                topics_arguments += "education=1"
            else:
                topics_arguments += "education=0"

            logging.debug(f"- topics_arguments: {topics_arguments}")
            url = f"http://localhost:9090/rs3a?{topics_arguments}"
            logging.debug(f"- url: {url}")
            response = requests.get(url)
            logging.debug(f"- response.status_code: {response.status_code}")
        except Exception as exception:
            message = f"{str(exception)}"
            raise cherrypy.HTTPError(500, message=message)

        return response

    @staticmethod
    def rs4a(
            analytical_percentage,
            anger_percentage,
            confident_percentage,
            fear_percentage,
            joy_percentage,
            sadness_percentage,
            tentative_percentage
    ):
        logging.debug(f"RecommendationSystem.rs4a("
                      f"analytical_percentage={analytical_percentage}, "
                      f"anger_percentage={anger_percentage}, "
                      f"confident_percentage={confident_percentage}, "
                      f"fear_percentage={fear_percentage}, "
                      f"joy_percentage={joy_percentage}, "
                      f"sadness_percentage={sadness_percentage}, "
                      f"tentative_percentage={tentative_percentage})")

        try:
            tone_arguments = f"analytical={(int(analytical_percentage) / 100)}&"
            tone_arguments += f"anger={(int(anger_percentage) / 100)}&"
            tone_arguments += f"confident={(int(confident_percentage) / 100)}&"
            tone_arguments += f"fear={(int(fear_percentage) / 100)}&"
            tone_arguments += f"joy={(int(joy_percentage) / 100)}&"
            tone_arguments += f"sadness={(int(sadness_percentage) / 100)}&"
            tone_arguments += f"tentative={(int(tentative_percentage) / 100)}"

            logging.debug(f"- tone_arguments: {tone_arguments}")
            url = f"http://localhost:9090/rs4a?{tone_arguments}"
            logging.debug(f"- url: {url}")
            response = requests.get(url)
            logging.debug(f"- response.status_code: {response.status_code}")
        except Exception as exception:
            message = f"{str(exception)}"
            raise cherrypy.HTTPError(500, message=message)

        return response
