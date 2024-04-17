from flask import *
import admin_DAO
import boto3
import pymysql
import requests

app = Flask(__name__)
app.secret_key = 'qwer!@!@'

# AWS 자격 증명 및 S3 클라이언트 생성
session2 = boto3.Session(

    region_name='us-east-2'
)
s3 = session2.client('s3')

def get_public_url(bucket_name, key):
    # S3 객체에 대한 공개적인 URL 생성
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': key},
        ExpiresIn=3600  # URL의 유효기간 설정 (초 단위)
    )
    return url

# @app.route('/test_lambda', methods=['GET'])
# def test_lambda():
#     # RDS 연결 정보
#     rds_host = "coupangdb.cg30bdkh6kth.ap-northeast-3.rds.amazonaws.com"
#     username = "root"
#     password = "admin12345"
#     db_name = "coupang"

#     try:
#         # RDS 연결
#         conn = pymysql.connect(host=rds_host,
#                                user=username,
#                                password=password,
#                                db=db_name,
#                                connect_timeout=5)
#         with conn.cursor() as cursor:
#             sql = "SELECT * FROM admin"
#             cursor.execute(sql)
#             result = cursor.fetchall()
#             # 필요에 따라 데이터 처리
#             data = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
#             print("테스트 1번")
#             print(data)
#             return jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}
#     except Exception as e:
#         print("ERROR: Unable to fetch data from RDS")
#         print(e)
#         return jsonify({'error': 'Unable to fetch data from RDS'}), 500
#     finally:
#         conn.close()

# AWS Lambda 함수의 API Gateway 엔드포인트 URL
lambda_endpoint_url = 'https://qaqxhieo7h.execute-api.us-east-2.amazonaws.com/getStage'
api_key = '7z5soUp1PD9783y5PENuL4fmlC3qGtIk5ij3U5Jy'
authorizer_id = 'd23dmr'
@app.route('/test_lambda')
def test_lambda():
    try:
        # AWS Lambda 함수의 API Gateway 엔드포인트로 GET 요청을 보냄.
        headers = {
            'x-api-key': api_key,
            'Authorization': authorizer_id  # 권한 부여자 ID를 헤더에 추가
        }
        response = requests.get(lambda_endpoint_url, headers=headers)

        # 응답 코드가 200이면 데이터를 JSON 형식으로 반환
        if response.status_code == 200:
            data = response.json()
            print(data)
            return jsonify(data)
        else:
            # 응답 코드가 200이 아니면 오류 메시지를 반환
            print(response)
            print(response.content)
            print(response.history)
            return f'Error: Unable to fetch data from Lambda function. Status code: {response.status_code}', 500
    except Exception as e:
        # 예외가 발생하면 오류 메시지를 반환
        return f'Error: {str(e)}', 500

            
# index 페이지
@app.route('/')
def home() :
    
    # return render_template('index.html')
    return redirect('/login')

# main 관리 페이지
@app.route('/main')
def main() :
    
    return render_template('main.html')

# 로그인
@app.route('/login', methods=['POST', 'GET'])
def login() :
    if request.method == 'GET' :

        return render_template('index.html')
    
    elif request.method == 'POST' :
        # Form에서 입력한 id
        userId = request.form['userId']
        # Form에서 입력한 password
        userPw = request.form['userPw']

        # Form에서 입력한 id를 기반으로 DB 검색
        userResult = admin_DAO.selectMemberById(userId)
        
        if userResult is not None :
            # Form에서 입력한 정보와 DB 정보 비교 후 일치하면 유저의 모든 정보를 Session에 저장
            if(userId == userResult['admin_id'] and userPw == userResult['admin_pw']) :
                session['loginSessionInfo'] = userResult
                return redirect(url_for('main'))
            else :
                return render_template('member/login_fail.html')
        else :
            return render_template('member/login_fail.html')
    else :
        return render_template('index.html')
    
# 로그아웃
@app.route('/logout')
def logout() :

    if 'loginSessionInfo' in session :
        session.pop('loginSessionInfo', None)
        return redirect(url_for('login'))
    else :
        return '<h2>User already logged out <a href="/login">Click here</a></h2>'
    
# 상품등록
@app.route('/register', methods=['POST', 'GET'])
def register() :
    if request.method == 'GET' :
        s3_bucket = "final-koupang-bucket"
        s3_image1 = "furtniture/test1.jpg"
        s3_image2 = "furtniture/test2.jpg"

        s3_image_url1 = get_public_url(s3_bucket, s3_image1)
        s3_image_url2 = get_public_url(s3_bucket, s3_image2)

        return render_template('admin/register.html', s3_image_url1=s3_image_url1, s3_image_url2=s3_image_url2)
    
    elif request.method == 'POST' :
        # Form에서 입력한 id
        userId = request.form['userId']
        # Form에서 입력한 password
        userPw = request.form['userPw']

        # Form에서 입력한 id를 기반으로 DB 검색
        userResult = admin_DAO.selectMemberById(userId)
        

    else :
        return render_template('index.html')
        
# main
if __name__ == '__main__' :
    app.run(debug=True)



