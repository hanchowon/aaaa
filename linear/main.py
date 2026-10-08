import os
from flask import Flask, request, jsonify

app = Flask(__name__)

def linear_search(arr, target):
    """
    선형검색 알고리즘 수행 함수
    :param arr: 검색 대상 리스트 (list)
    :param target: 찾고자 하는 값 (int, float, str 등)
    :return: (찾은 인덱스, 단계별 추적 데이터 리스트)
    """
    steps = []
    found_index = -1

    # 리스트의 첫 번째 요소부터 순차적으로 탐색
    for idx, value in enumerate(arr):
        # 형변환 시 발생할 수 있는 차이를 방지하기 위해 문자열 비교로 정규화
        is_match = str(value).strip() == str(target).strip()
        
        # 각 탐색 단계를 기록 (클라이언트 시각화를 위한 정보)
        steps.append({
            "step": idx + 1,           # 현재 단계 번호 (1-based)
            "currentIndex": idx,       # 현재 검사 중인 배열 인덱스
            "currentValue": value,     # 현재 인덱스의 값
            "isMatch": is_match        # 타깃과 일치하는지 여부
        })

        if is_match:
            found_index = idx
            break  # 값 찾으면 즉시 검색 종료

    return found_index, steps

@app.route('/search', methods=['POST'])
def handle_search():
    """
    선형검색 HTTP POST 요청 처리 엔드포인트
    Request JSON Body:
      {
        "array": [10, 20, 30, 40, 50],
        "target": 30
      }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "요청 Body가 비어있습니다."}), 400

        arr = data.get("array", [])
        target = data.get("target", None)

        if not isinstance(arr, list) or target is None:
            return jsonify({"status": "error", "message": "'array'(배열)와 'target'(찾을 값) 필수 입력 요소입니다."}), 400

        # 선형검색 실행 및 단계 데이터 수집
        found_index, steps = linear_search(arr, target)

        # 결과 데이터 응답
        return jsonify({
            "status": "success",
            "serverInfo": "Google Cloud Run (Python Flask)",
            "array": arr,
            "target": target,
            "foundIndex": found_index,
            "isFound": found_index != -1,
            "totalSteps": len(steps),
            "steps": steps,
            # 알고리즘 복잡도 정보 반환
            "complexity": {
                "time": "O(N)",
                "space": "O(1)",
                "description": "선형검색은 최악의 경우 N번의 비교를 수행하므로 시간 복잡도는 O(N)입니다."
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"서버 처리 중 오류 발생: {str(e)}"}), 500

# 헬스체크 엔드포인트
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Linear Search Service running on Cloud Run"}), 200

if __name__ == '__main__':
    # Cloud Run에서 제공하는 PORT 환경 변수 사용 (기본값: 8080)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
