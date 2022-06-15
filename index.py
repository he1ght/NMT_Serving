from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)
board = []

from realtime_generate import translate

@app.route('/')
def index():
    return render_template('list.html', rows=board)


# 게시판 내용 추가 (Create)
@app.route('/add', methods=["POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        context = request.form["context"]
        board.append([name, context])
        return redirect(url_for("index"))
    else:
        return render_template("list.html", rows=board)


# 게시판 내용 갱신 (Update)
@app.route('/update/<int:uid>', methods=["GET", "POST"])
def update(uid):
    if request.method == "POST":
        index = uid - 1
        name = request.form["name"]
        context = request.form["context"]

        board[index] = [name, context]  # 기존의 board내용에 덮어쓰기
        return redirect(url_for("index"))
    else:
        return render_template("update.html", index=uid, rows=board)


# 게시판 내용 삭제 (Delete)
@app.route('/delete/<int:uid>')
def delete(uid):
    index = uid - 1
    del board[index]

    return redirect(url_for("index"))


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