from multiprocessing import Process

from .mallet_topics import run

@app.route("/")
def exampleMethod():
    # Make the scraping asynchronous for not timing out the http-request
    p = Process(target=run) #args=('bob',)
    p.start()
    return "Started MALLET run"
