import streamlit as st
from streamlit_ace import st_ace
import json
import contextlib
import io
from pathlib import Path

# ---------------------------
# 💾 永続化ヘルパー
# ---------------------------
PROGRESS_FILE = Path("progress.json")

def load_progress():
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_progress(progress):
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"進捗の保存に失敗しました: {e}")

# ---------------------------
# 📝 問題定義
# ---------------------------
PROBLEMS = [
    {
        "id": "prime",
        "title": "素数判定",
        "points": 10,
        "description": "整数 n が素数であれば True、そうでなければ False を返す関数 is_prime(n) を実装してください。",
        "function_name": "is_prime",
        "template": """def is_prime(n):\n    # ここに実装\n    pass\n""",
        "tests": {
            2: True,
            3: True,
            4: False,
            5: True,
            9: False,
            13: True,
            20: False,
            29: True,
        },
    },
    {
        "id": "fizzbuzz",
        "title": "FizzBuzz",
        "points": 10,
        "description": "1 以上 n 以下の整数を順に処理し、3 の倍数のとき \"Fizz\"、5 の倍数のとき \"Buzz\"、両方の倍数のとき \"FizzBuzz\"、それ以外は数値文字列を返す関数 fizzbuzz(n) を実装してください。戻り値はリストで。",
        "function_name": "fizzbuzz",
        "template": """def fizzbuzz(n):\n    # ここに実装\n    pass\n""",
        "tests": {
            5: ["1", "2", "Fizz", "4", "Buzz"],
            15: ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"],
        },
    },
    {
        "id": "factorial",
        "title": "階乗計算",
        "points": 10,
        "description": "非負整数 n の階乗 n! を返す関数 factorial(n) を実装してください（0! = 1）。",
        "function_name": "factorial",
        "template": """def factorial(n):\n    # ここに実装\n    pass\n""",
        "tests": {0: 1, 1: 1, 3: 6, 5: 120, 8: 40320},
    },
]

PROBLEM_MAP = {p["id"]: p for p in PROBLEMS}

# ---------------------------
# 🌟 Streamlit UI
# ---------------------------
st.set_page_config(page_title="Coding Quiz", page_icon="💻", layout="wide")

# セッション状態初期化
if "progress" not in st.session_state:
    st.session_state.progress = load_progress()

progress = st.session_state.progress

# サイドバー: 問題選択
st.sidebar.title("🗂️ 問題リスト")
problem_options = {p["title"]: p["id"] for p in PROBLEMS}
selected_title = st.sidebar.radio("解く問題を選択", list(problem_options.keys()))
current_problem_id = problem_options[selected_title]
current_problem = PROBLEM_MAP[current_problem_id]

# メインエリア: 問題内容
st.title(current_problem["title"])
st.markdown(current_problem["description"])

# 進捗表示
solved_count = sum(1 for pid in progress if progress[pid].get("solved"))
max_score = sum(p["points"] for p in PROBLEMS)
current_score = sum(progress.get(pid, {}).get("score", 0) for pid in progress)
col1, col2 = st.columns(2)
col1.metric("✅ 解決済み問題", f"{solved_count}/{len(PROBLEMS)}")
col2.metric("🏅 スコア", f"{current_score}/{max_score}")

# コードエディター
code_key = f"code_{current_problem_id}"
if code_key not in st.session_state:
    # 以前のコードがあればロード、なければテンプレート
    st.session_state[code_key] = progress.get(current_problem_id, {}).get("code", current_problem["template"])

user_code = st_ace(
    value=st.session_state[code_key],
    language="python",
    theme="monokai",
    keybinding="vscode",
    font_size=14,
    tab_size=4,
    height=350,
    auto_update=True,
)

st.session_state[code_key] = user_code  # 更新

# コード検証
if st.button("🚀 コードを検証", key=f"test_{current_problem_id}"):
    namespace = {}
    with contextlib.redirect_stdout(io.StringIO()) as f:
        try:
            exec(user_code, namespace)
        except Exception as e:
            st.error(f"コード実行中にエラーが発生しました: {e}")
            st.stop()

    func = namespace.get(current_problem["function_name"])
    if func is None or not callable(func):
        st.error(f"関数 `{current_problem['function_name']}` が定義されていません。")
        st.stop()

    all_passed = True
    for inp, expected in current_problem["tests"].items():
        try:
            result = func(inp)
            if result != expected:
                st.warning(f"❌ 入力: {inp} → {result} (期待値: {expected})")
                all_passed = False
            else:
                st.info(f"✅ 入力: {inp} → {result}")
        except Exception as e:
            st.error(f"❌ 入力: {inp} 実行時にエラー: {e}")
            all_passed = False

    # スコア計算・保存
    if current_problem_id not in progress:
        progress[current_problem_id] = {}

    progress[current_problem_id]["code"] = user_code

    if all_passed:
        if not progress[current_problem_id].get("solved"):
            progress[current_problem_id]["solved"] = True
            progress[current_problem_id]["score"] = current_problem["points"]
            st.balloons()
            st.success(f"🎉 すべてのテストに合格しました！ +{current_problem['points']} ポイント獲得")
        else:
            st.success("既にこの問題は解決済みです。")
    else:
        progress[current_problem_id]["solved"] = False
        progress[current_problem_id]["score"] = 0
        st.warning("テストに不合格です。再挑戦してください！")

    save_progress(progress)

# サイドバー: 進捗詳細
st.sidebar.markdown("---")
st.sidebar.subheader("📊 進捗状況")
for p in PROBLEMS:
    pid = p["id"]
    status = "✅" if progress.get(pid, {}).get("solved") else "🔸"
    points = progress.get(pid, {}).get("score", 0)
    st.sidebar.write(f"{status} {p['title']} — {points}/{p['points']} pt")

# フッター
st.markdown("---")
st.markdown("Made with Streamlit & Ace • Happy coding! 🐍💻")
