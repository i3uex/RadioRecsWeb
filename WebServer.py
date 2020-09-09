import json
import uuid

import cherrypy

import engine


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
class GetOptionsService(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        """
        Serves the data needed to render the home page
        """
        return json.dumps({
            'default_datasets': engine.get_default_datasets(),
            'transformations': engine.get_transformations()
        })


@cherrypy.expose
class SetOptionsService(object):
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, options):
        """
        Receives the data needed to perform a transformation, returns the
        result of said transformation
        """
        options = json.loads(options)

        try:
            result = engine.execute(
                options['dataset_name'],
                options['dataset_path'],
                options['dataset_contents'],
                options['transformation_category'],
                options['transformation'],
                options['arguments']
            )
        except Exception as exception:
            message = f"{str(exception)}"
            raise cherrypy.HTTPError(500, message=message)

        return result

@cherrypy.expose
@cherrypy.tools.json_out()
class GetDefaultDatasetHeadersService(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, default_dataset_name):
        return {'headers': engine.get_default_dataset_headers(default_dataset_name)}
