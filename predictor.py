import json
import logging
from decimal import Decimal

import cherrypy
import pandas
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
            programs,
            voice_music_weight,
            genres_weight,
            topics_weight,
            tones_weight
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
                      f"programs={programs}, "
                      f"voice_music_weight={voice_music_weight}, "
                      f"genres_weight={genres_weight}, "
                      f"topics_weight={topics_weight}, "
                      f"tones_weight={tones_weight})")

        try:
            voice_percentage = int(voice_percentage) / 100
            music_percentage = 1 - voice_percentage
            analytical_percentage = int(analytical_percentage) / 100
            anger_percentage = int(anger_percentage) / 100
            confident_percentage = int(confident_percentage) / 100
            fear_percentage = int(fear_percentage) / 100
            joy_percentage = int(joy_percentage) / 100
            sadness_percentage = int(sadness_percentage) / 100
            tentative_percentage = int(tentative_percentage) / 100

            rs1a_response = RecommendationSystem.rs1a(
                music_percentage, voice_percentage
            )
            rs2a_response = RecommendationSystem.rs2a(
                music_genres
            )
            rs3a_response = RecommendationSystem.rs3a(
                topics
            )
            rs4a_response = RecommendationSystem.rs4a(
                analytical_percentage,
                anger_percentage,
                confident_percentage,
                fear_percentage,
                joy_percentage,
                sadness_percentage,
                tentative_percentage
            )

            logging.debug(f"- rs1a_response: {rs1a_response}")
            logging.debug(f"- rs2a_response: {rs2a_response}")
            logging.debug(f"- rs3a_response: {rs3a_response}")
            logging.debug(f"- rs4a_response: {rs4a_response}")

            rs1a_dataframe = pandas.read_json(rs1a_response.text, orient="records")
            rs2a_dataframe = pandas.read_json(rs2a_response.text, orient="records")
            rs3a_dataframe = pandas.read_json(rs3a_response.text, orient="records")
            rs4a_dataframe = pandas.read_json(rs4a_response.text, orient="records")

            program_names_string = programs[0]
            if program_names_string != "":
                programs_name_list = program_names_string.replace(",", "|")
                programs = RecommendationSystem.get_programs(programs_name_list)

                rs1b_response = RecommendationSystem.rsb(1, programs)
                rs2b_response = RecommendationSystem.rsb(2, programs)
                rs3b_response = RecommendationSystem.rsb(3, programs)
                rs4b_response = RecommendationSystem.rsb(4, programs)

                rs1b_dataframe = pandas.read_json(rs1b_response.text, orient="records")
                rs2b_dataframe = pandas.read_json(rs2b_response.text, orient="records")
                rs3b_dataframe = pandas.read_json(rs3b_response.text, orient="records")
                rs4b_dataframe = pandas.read_json(rs4b_response.text, orient="records")
            else:
                rs1b_dataframe = rs1a_dataframe.copy()
                rs2b_dataframe = rs1a_dataframe.copy()
                rs3b_dataframe = rs1a_dataframe.copy()
                rs4b_dataframe = rs1a_dataframe.copy()

            rs2a_dataframe.drop(["_nombre"], axis=1, inplace=True)
            rs3a_dataframe.drop(["_nombre"], axis=1, inplace=True)
            rs4a_dataframe.drop(["_nombre"], axis=1, inplace=True)
            rs1b_dataframe.drop(["_nombre"], axis=1, inplace=True)
            rs2b_dataframe.drop(["_nombre"], axis=1, inplace=True)
            rs3b_dataframe.drop(["_nombre"], axis=1, inplace=True)
            rs4b_dataframe.drop(["_nombre"], axis=1, inplace=True)

            weights_dataframe = pandas.concat([
                rs1a_dataframe,
                rs1b_dataframe,
                rs2a_dataframe,
                rs2b_dataframe,
                rs3a_dataframe,
                rs3b_dataframe,
                rs4a_dataframe,
                rs4b_dataframe
            ], axis=1)
            weights_dataframe.columns = [
                "program_name",
                "wrs1a",
                "wrs1b",
                "wrs2a",
                "wrs2b",
                "wrs3a",
                "wrs3b",
                "wrs4a",
                "wrs4b"
            ]
            weights_dataframe.set_index("program_name", inplace=True)
            weights_dataframe["wrs1"] = (weights_dataframe["wrs1a"] + weights_dataframe["wrs1b"]) / 2
            weights_dataframe["wrs2"] = (weights_dataframe["wrs2a"] + weights_dataframe["wrs2b"]) / 2
            weights_dataframe["wrs3"] = (weights_dataframe["wrs3a"] + weights_dataframe["wrs3b"]) / 2
            weights_dataframe["wrs4"] = (weights_dataframe["wrs4a"] + weights_dataframe["wrs4b"]) / 2

            weights_dataframe["wrs"] = \
                0.25 * weights_dataframe["wrs1"] + \
                0.75 * (
                        music_percentage * weights_dataframe["wrs2"] +
                        voice_percentage * (weights_dataframe["wrs3"] + weights_dataframe["wrs4"]) / 2
                )
            weights_dataframe.sort_values(by=["wrs"], ascending=False, inplace=True)
            recommended_program_names = weights_dataframe.index.values.tolist()[:20]
            recommended_program_weights = weights_dataframe["wrs"].tolist()[:20]

            result = {}
            for index, recommended_program_name in enumerate(recommended_program_names):
                recommended_program_weight = Decimal(recommended_program_weights[index]).quantize(Decimal(10) ** -5)
                # result.append(f"{recommended_program_name} <sub>{recommended_program_weight}</sub>")
                result[recommended_program_name] = str(recommended_program_weight)

            logging.debug(f"- rs1a_dataframe: {rs1a_dataframe.describe()}")
            logging.debug(f"- rs1b_dataframe: {rs1b_dataframe.describe()}")
            logging.debug(f"- rs2a_dataframe: {rs2a_dataframe.describe()}")
            logging.debug(f"- rs2b_dataframe: {rs2b_dataframe.describe()}")
            logging.debug(f"- rs3a_dataframe: {rs3a_dataframe.describe()}")
            logging.debug(f"- rs3b_dataframe: {rs3b_dataframe.describe()}")
            logging.debug(f"- rs4a_dataframe: {rs4a_dataframe.describe()}")
            logging.debug(f"- rs4b_dataframe: {rs4b_dataframe.describe()}")

            logging.debug(f"- weights_dataframe: {weights_dataframe.describe()}")

        except Exception as exception:
            message = f"{str(exception)}"
            raise Exception(message)

        return json.dumps(result)

    @staticmethod
    def rs1a(music_percentage, voice_percentage):
        logging.debug(f"RecommendationSystem.rs1a("
                      f"voice_percentage={voice_percentage})")

        try:
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
            url = "http://localhost:9090/rs2a"
            if music_genres[0] != "":
                music_genres_list = music_genres[0].split(",")
                music_genres_argument = ""
                for music_genre in music_genres_list:
                    logging.debug(f"- music_genre: {music_genre}")
                    music_genres_argument += f"{music_genre}=1&"
                if music_genres_argument != "":
                    music_genres_argument = music_genres_argument[:-1]
                logging.debug(f"- music_genres_argument: {music_genres_argument}")
                url = f"{url}?{music_genres_argument}"
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
            url = "http://localhost:9090/rs3a"
            if topics[0] != "":
                topics_list = topics[0].split(",")
                topics_arguments = ""

                if "news" in topics_list:
                    topics_arguments += "news=1&"
                else:
                    topics_arguments += "news=0&"

                if "sport" in topics_list:
                    topics_arguments += "sport=1&"
                else:
                    topics_arguments += "sport=0&"

                if "entertainment" in topics_list:
                    topics_arguments += "entertainment=1&"
                else:
                    topics_arguments += "entertainment=0&"

                if "musical" in topics_list:
                    topics_arguments += "musical=1&"
                else:
                    topics_arguments += "musical=0&"

                if "education" in topics_list:
                    topics_arguments += "education=1"
                else:
                    topics_arguments += "education=0"

                logging.debug(f"- topics_arguments: {topics_arguments}")
                url = f"{url}?{topics_arguments}"
            logging.debug(f"- url: {url}")
            response = requests.get(url)
            logging.debug(f"- response.status_code: {response.status_code}")
        except Exception as exception:
            message = f"{str(exception)}"
            raise Exception(message)

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

    @staticmethod
    def get_programs(program_names):
        logging.debug(f"RecommendationSystem.get_programs("
                      f"program_names={program_names})")

        try:
            url = f"http://localhost:9090/programs?like={program_names}"
            logging.debug(f"- url: {url}")
            response = requests.get(url)
            logging.debug(f"- response.status_code: {response.status_code}")
        except Exception as exception:
            message = f"{str(exception)}"
            raise cherrypy.HTTPError(500, message=message)

        return json.loads(response.text)

    @staticmethod
    def rsb(service, programs):
        logging.debug(f"RecommendationSystem.rsb("
                      f"service={service}, "
                      f"programs={programs})")

        try:
            program_list = '|'.join(programs)
            url = f"http://localhost:9090/rs{service}b?like={program_list}"
            logging.debug(f"- url: {url}")
            response = requests.get(url)
            logging.debug(f"- response.status_code: {response.status_code}")
        except Exception as exception:
            message = f"{str(exception)}"
            raise cherrypy.HTTPError(500, message=message)

        return response

    @staticmethod
    def calculate_weight(row):
        music_percentage = 0.5
        voice_percentage = 0.5
        return 0.25 * row["wrs1a"] + \
               0.75 * (music_percentage * row["wrs2a"] + voice_percentage * (row["wrs3a"] + row["wrs4a"]) / 2)
