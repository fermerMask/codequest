import streamlit as st
from streamlit_ace import st_ace
import contextlib
import io

# ---------------------------
# 問題定義
# ---------------------------
PROBLEMS = [
    {
        "id": "prime",
        "title": "素数判定",
        "description": "整数 n が素数であれば True、そうでなければ False を返す関数 is_prime(n) を実装してください。",
        "function_name": "is_prime",
        "template": """def is_prime(n):\n    # ここに実装\n    """,
        "inputs": [[2, 3, 4, 5, 9, 13, 20, 29]],
        "ideal_outputs":[['True',"True","False","True","False","True","False","True"]],
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
        "description": "1 以上 n 以下の整数を順に処理し、3 の倍数のとき \"Fizz\"、5 の倍数のとき \"Buzz\"、両方の倍数のとき \"FizzBuzz\"、それ以外は数値文字列を返す関数 fizzbuzz(n) を実装してください。",
        "function_name": "fizzbuzz",
        "template": """def fizzbuzz(n):\n    # ここに実装\n    """,
        "inputs": [[5, 15]],
        "ideal_outputs": [["5 : 1, 2, Fizz, 4, Buzz"], ["15: 1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz"]],
        "tests": {
            5: ["1", "2", "Fizz", "4", "Buzz"],
            15: ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
        },
    },
    {
        "id": "file_format",
        "title": "ファイル名整形",
        "description": "リストで与えられたファイル名を `YYYYMMDD_description.txt` の形式に整形して返す関数 format_filenames(filenames) を実装してください。",
        "function_name": "format_filenames",
        "template": """from datetime import datetime\ndef format_filenames(filenames):\n    # ここに実装\n    """,
        "inputs":[["2023-01-01 report.txt", "2023-01-02 notes.txt","2024-05-27 log.csv", "2024-06-01 memo.txt"]],
        "ideal_outputs":[["20230101_report.txt", "20230102_notes.txt"],["20240527_log.csv", "20240601_memo.txt"]],
        "tests": {
            tuple(["2023-01-01 report.txt", "2023-01-02 notes.txt"]): ["20230101_report.txt", "20230102_notes.txt"],
            tuple(["2024-05-27 log.csv", "2024-06-01 memo.txt"]): ["20240527_log.csv", "20240601_memo.txt"],
        },
    },
]

PROBLEM_MAP = {p["id"]: p for p in PROBLEMS}

st.set_page_config(page_title="Coding Quiz", page_icon="💻", layout="wide")

st.sidebar.title("📚 モード選択")
mode = st.sidebar.radio("表示モードを選択", ["問題に挑戦", "Python練習モード"])

if mode == "Python練習モード":
    st.title("Python練習モード")
    st.header("pythonを自由に書いて動かすことができるモードです")
    with st.expander("🧠 Pythonの基本を学ぼう（クリックで展開）"):
        st.markdown("""### 🐍 Pythonとは？
                    Python（パイソン）は、読みやすくて書きやすいプログラミング言語です。初心者にも優しく、データ分析やWeb開発、AIにも広く使われています。
                    Pythonは気軽に利用することができ，特にプログラミングが始めてという方に最適な言語です。事実，大学や専門学校などのコンピュータサイエンスの授業では
                    最初の言語としてPythonを採用することが多くあります。
                    """
                    )
    with st.expander("🧩 基本の説明（クリックで展開）"):
        st.markdown("""
  #### ✅ 変数（variable）
    値を保存しておくための名前付きの箱です：
    ```python
    name = "Alice"
    age = 25
    ```

    #### ✅ 関数（function）
    何度も使う処理をまとめておく箱のようなもの：
    ```python
    def greet(name):
        return f"Hello, {name}!"
    ```

    #### ✅ 条件分岐（if文）
    条件によって処理を変える：
    ```python
    if age >= 20:
        print("成人です")
    else:
        print("未成年です")
    ```

    #### ✅ ループ（for文）
    同じ処理を何度も繰り返す：
    ```python
    for i in range(3):
        print(i)
    ```

    ### ✨ サンプルコードを試してみましょう！
    ```python
    name = "Taro"
    print(greet(name))
    ```
""")
    with st.expander("サンプルコード一覧"):
        st.markdown("""
### サンプル１；名前を使って挨拶をする関数
```python
def greet(name):
    return f"こんにちは{name}}さん！
print(greet("太郎"))
```                   
### サンプル２：偶数か奇数か判定
```python
n = 7
if n % 2 == 0:
    print(f"{n}は偶数です")
else:
    print(f"{n}"は奇数です
```
### サンプル３：１～５の合計を求めるループ
```python
total = 0
for i in range(1,6):
    total += i
print(f"合計は{total}です")
```                    
""")
    code = st_ace(language="python", theme="monokai", font_size=14, tab_size=4, height=300)
    if st.button("▶ 実行"):
        try:
            with contextlib.redirect_stdout(io.StringIO()) as f:
                exec(code, {})
            st.success("✅ 実行結果:")
            st.code(f.getvalue())
        except Exception as e:
            st.error(f"❌ エラー: {e}")
else:
    # 問題ページ
    st.sidebar.title("🗂️ 問題リスト")
    problem_options = {p["title"]: p["id"] for p in PROBLEMS}
    selected_title = st.sidebar.radio("解く問題を選択", list(problem_options.keys()))
    current_problem_id = problem_options[selected_title]
    current_problem = PROBLEM_MAP[current_problem_id]

    st.title(current_problem["title"])
    st.markdown(f"**説明** : {current_problem["description"]}")
    
    st.markdown(''' **入力例** 実際にここに表示されている値が入力されます''')
    for example in current_problem.get("inputs"):
        st.code(str(example))
    
    st.markdown(''' **解答例** ''')
    for result in current_problem.get("ideal_outputs"):
        st.code(str(result))

    code_key = f"code_{current_problem_id}"
    if code_key not in st.session_state:
        st.session_state[code_key] = current_problem["template"]

    if st.button("テンプレートに戻す"):
        st.session_state[code_key] = current_problem['template']
        st.rerun()

    user_code = st_ace(
        key=code_key,
        value=st.session_state[code_key],
        language="python",
        theme="monokai",
        keybinding="vscode",
        font_size=14,
        tab_size=4,
        height=350,
        auto_update=False,
    )

    if user_code is not None and user_code != st.session_state[code_key]:
        st.session_state[code_key] = user_code

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
                result = func(list(inp) if isinstance(inp, tuple) else inp)
                if result != expected:
                    st.warning(f"❌ 入力: {inp} → {result} (期待値: {expected})")
                    all_passed = False
                else:
                    st.info(f"✅ 入力: {inp} → {result}")
            except Exception as e:
                st.error(f"❌ 入力: {inp} 実行時にエラー: {e}")
                all_passed = False

        if all_passed:
            st.balloons()
            st.success("🎉 すべてのテストに合格しました！")
