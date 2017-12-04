# dmx lighting control
# Ben Hussey - Oct 17
from bottle import route, run, HTTPError
from fixture_manager import Manager

manager = Manager(debug=True)
manager.set_state('1')
manager.transition()
manager.set_state('99')


@route('/level/<fixture>/<level>/')
def level(fixture, level):
    if fixture not in manager.fixtures:
        return HTTPError(404, "Page not found")
    manager.fixtures[fixture].set_level(int(level))
    manager.change()


@route('/color/<fixture>/<color>/')
def color(fixture, color):
    if fixture not in manager.fixtures:
        return HTTPError(404, "Page not found")
    manager.fixtures[fixture].set_color(color)
    manager.change()


@route('/state/<state>/')
def state(state):
    manager.set_state(state)
    manager.transition()


run(host='0.0.0.0', port=8000, debug=True, threaded=True)
