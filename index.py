import subprocess

from flask import Flask, request, jsonify, render_template, redirect, url_for, Response, flash

from tts import synthesize_text_file

app = Flask(__name__)
board = []

from realtime_generate import translate

@app.route('/')
def index():
    return render_template('init.html', rows=board)


@app.route('/web_trans', methods=["POST"])
def web_trans():
    if request.method == "POST":
        context = request.form["context"]
        result = translate(context)
        board.append([context, result])
        return redirect(url_for("index"))
    else:
        return render_template("init.html", rows=board)

def generate(audio_bin):

    #  get_list_all_files_name this function gives all internal files inside the folder

    filesAudios = audio_bin # get_list_all_files_name(currentDir + "/streamingAudios/1")

    # audioPath is audio file path in system
    for audioPath in filesAudios:
        data = subprocess.check_output(['cat', audioPath])
        yield data

@app.route('/web_speak_original')
def web_speak_original():
    context = request.form["context"]

    audio_bin = synthesize_text_file(context)

    # return Response(generate(audio_bin), mimetype='audio/mp3')
    return Response(audio_bin, mimetype='audio/mp3')


# @app.route('/web_speak', methods=["POST"])
# def web_speak():
#     if request.method == "POST":
#         result = request.form["result"]
#         return redirect(url_for("index"))
#     else:
#         return render_template("init.html", rows=board)

# @app.route('/update/<int:uid>', methods=["GET", "POST"])
# def update(uid):
#     if request.method == "POST":
#         index = uid - 1
#         name = request.form["name"]
#         context = request.form["context"]
#
#         board[index] = [name, context]  # 기존의 board내용에 덮어쓰기
#         return redirect(url_for("index"))
#     else:
#         return render_template("update.html", index=uid, rows=board)

@app.route('/speak/<int:uid>')
def speak(uid):
    index = uid - 1
    context = board[index][1]
    audio_bin = synthesize_text_file(context)

    # return Response(generate(audio_bin), mimetype='audio/mp3')
    return Response(audio_bin, mimetype='audio/mp3')


@app.route('/delete/<int:uid>')
def delete(uid):
    index = uid - 1
    del board[index]

    return redirect(url_for("index"))

@app.route('/clear', methods=["POST"])
def clear():
    global board
    index = 0
    board = []
    # return redirect(url_for("index"))
    return render_template("init.html", rows=board)



@app.route("/utter_translate", methods=['POST'])
def utter_translate():
    req = request.get_json()

    # animal_type = req["action"]["detailParams"]["Animal_type"]["value"]	# json파일 읽기
    params = req["action"]["detailParams"]
    utter = req['userRequest']['utterance']
    # print(params)
    # print(utter)
    translation = translate(utter)

    answer = utter  # animal_type

    # 답변 텍스트 설정
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": translation
                    }
                }
            ]
        }
    }

    # 답변 전송
    return jsonify(res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)