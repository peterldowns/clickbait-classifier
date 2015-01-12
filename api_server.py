from flask import Flask, request, jsonify

print 'Loading classifier...'
import classifier

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def main(path):
    
    if 'q' not in request.args:
        return jsonify(status_code=400,
                       msg="Missing parameter 'q'")

    q = request.args.get('q')
    res = classifier.classify(q)

    return jsonify(**res)

if __name__ == '__main__':
    app.run()
