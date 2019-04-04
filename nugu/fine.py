from flask import (Flask,  request)
import json
app = Flask(__name__)
import pandas as pd
import numpy as np
import datetime,time

airplan_dic = {'서울':0,'부산':1,'제주':2}

name_box_kor_dic = {
    "수서":1,"동찬":2,"지제":3,"천안아산":4,"오송":5,"대전":6,
    "김천(구미)":7,"동대구":8,"신경주":9,"울산(통도사)":10,
    "부산":11,"공주":12,"익산":13,"정읍":14,"광주송정":15,"나주":16,
    "목포":17
}
name_box_kor_fix_dic ={
    '동찬에서':'동찬','동찬까지':'동찬','지제에서':'지제','지제까지':'지제','오송에서':'오송','오송까지':'오송','김천에서':'김천(구미)','김천까지':'김천(구미)','구미에서':'김천(구미)','구미까지':'김천(구미)',
    '신경주에서':'신경주','신경주까지':'신경주','경주에서':'신경주','경주까지':'신경주','공주까지':'공주','공주에서':'공주','익산까지':'익산','익산에서':'익산','정읍에서':'정읍','정읍까지':'정읍',
    '광주에서':'광주송정','광주까지':'광주송정','송정에서':'광주송정','송정까지':'광주송정','나주에서':'나주','나주까지':'나주','목포에서':'목포','목포까지':'목포',
    '부산에서':'부산', '부산까지':'부산', '동대구에서':'동대구','동대구까지':'동대구','수서에서':'수서','수서까지':'수서','대전까지':'대전','대전에서':'대전',
    '천안까지':'천안아산','천안에서':'천안아산','아산까지':'천안아산','아산에서':'천안아산','울산까지':'울산(통도사)','울산에서':'울산(통도사)','광주송정까지':'광주송정','광주송정에서':'광주송정',

}
name_box = ["Suseo","Dongchan","Jiji","Cheonan(Asan)","Osong","Daejeon","Gimcheon(Gumi)","Dongdaegu","ShinKyungju","Ulsan(Tongdosa)","Busan","Gongju","Iksan","Jeong-eup","Gwangju(Songje)","Naju","Mokpo"]

date_time_dic = {'TOMORROW': 'tomorrow', 'A_TOMORROW': 'tomorrowAdd', 'TODAY': 'today'}

date_time_kor_dic = {'tomorrow':'내일','tomorrowAdd':'모레','today':'오늘'}

def live_airplan_info(req,user,arrived):
    user_depart = user
    user_arrived = arrived
    airplan_dic = {'서울': 0, '부산': 1, '제주': 2}
    air_type_result, air_time_result, air_price_result = [], [], []
    airplan_live = pd.read_csv('airplan/trip_airplan_0_%s_%s.csv' % (airplan_dic[user_depart], airplan_dic[user_arrived]))
    cknow = datetime.datetime.now()
    ch, cm = cknow.hour, cknow.minute
    airplan_live['depart_time_scecond'] = airplan_live['depart_time_hour'] * 60 + airplan_live['depart_time_minute']
    airplan_live = airplan_live.loc[(airplan_live['depart_time_scecond'] >= ch * 60 + cm)]
    find_index = airplan_live.index
    if len(find_index) < 3:
        for i in range(len(find_index)):
            find_index = airplan_live.index[i]
            air_type = airplan_live.loc[find_index][0]
            time = airplan_live.loc[find_index][1]
            price = airplan_live.loc[find_index][2]
            air_type_result.append(air_type)
            air_time_result.append(time)
            air_price_result.append(str(price))
        if len(air_type_result) == 2:
            air_type_result.append('black')
            air_time_result.append('black')
            air_price_result.append('black')
        else:
            for i in range(2):
                air_type_result.append('black')
                air_time_result.append('black')
                air_price_result.append('black')
    else:
        for i in range(3):
            find_index = airplan_live.index[i]
            air_type = airplan_live.loc[find_index][0]
            time = airplan_live.loc[find_index][1]
            price = airplan_live.loc[find_index][2]
            air_type_result.append(air_type)
            air_time_result.append(time)
            air_price_result.append(str(price))
    print(air_type_result, air_time_result, air_price_result)
    print(type(air_type_result[0]),type(air_time_result[0]),type(air_price_result[0]))
    resp = {
        'version': "2.0",
        "resultCode": "OK",
        "output": {
            "air_time_1": air_time_result[0],
            "air_time_2": air_time_result[1],
            "air_time_3":air_time_result[2],
            "air_type_1": air_type_result[0],
            "air_type_2": air_type_result[1],
            "air_type_3":air_type_result[2],
            "air_price_1":air_price_result[0],
            "air_price_2":air_price_result[1],
            "air_price_3":air_price_result[2],
        }
    }
    return json.dumps(resp, ensure_ascii=False, indent=4)



def want_airplan_day(req,depart,arrived,when,hour):
    user_depart = depart
    user_arrived = arrived
    user_when = when
    user = int(hour)
    airplan_dic = {'서울': 0, '부산': 1, '제주': 2}
    air_type_result, air_time_result, air_price_result = [], [], []
    if user_when == '오후':
        want_hour = user + 12
    else:
        want_hour = user
    airplan_live = pd.read_csv('airplan/trip_airplan_0_%s_%s.csv' % (airplan_dic[user_depart], airplan_dic[user_arrived]))
    print(airplan_live.shape)
    # airplan_live = airplan_live['']
    airplan_live['depart_time_scecond'] = airplan_live['depart_time_hour'] * 60 + airplan_live['depart_time_minute']
    airplan_live = airplan_live.loc[(airplan_live['depart_time_scecond'] >= want_hour * 60 + 0)]
    find_index = airplan_live.index
    if len(find_index) < 3:
        for i in range(len(find_index)):
            find_index = airplan_live.index[i]
            air_type = airplan_live.loc[find_index][0]
            time = airplan_live.loc[find_index][1]
            price = airplan_live.loc[find_index][2]
            air_type_result.append(air_type)
            air_time_result.append(time)
            air_price_result.append(str(price))
        if len(air_type_result) == 2:
            air_type_result.append('black')
            air_time_result.append('black')
            air_price_result.append('black')
        else:
            for i in range(2):
                air_type_result.append('black')
                air_time_result.append('black')
                air_price_result.append('black')
    else:
        for i in range(3):
            find_index = airplan_live.index[i]
            air_type = airplan_live.loc[find_index][0]
            time = airplan_live.loc[find_index][1]
            price = airplan_live.loc[find_index][2]
            air_type_result.append(air_type)
            air_time_result.append(time)
            air_price_result.append(str(price))

    resp = {
        'version': "2.0",
        "resultCode": "OK",
        "output": {
            "air_time_4": air_time_result[0],
            "air_time_5": air_time_result[1],
            "air_time_6":air_time_result[2],
            "air_type_4": air_type_result[0],
            "air_type_5": air_type_result[1],
            "air_type_6": air_type_result[2],
            "air_price_4": air_price_result[0],
            "air_price_5": air_price_result[1],
            "air_price_6":air_price_result[2],
        }
    }
    return json.dumps(resp, ensure_ascii=False, indent=4)


def want_day_airplan_lowprice(req,depart,arrived,wants_Day):
    user_depart = depart  # 유저가 출발할 도시
    user_arrived = arrived  # 유저가 도착할 도시
    user_day = int(wants_Day)  # 유저가 몇일뒤에 가고 싶은 날
    airplan_dic = {'서울': 0, '부산': 1, '제주': 2}
    air_type_result, air_time_result, air_price_result = [], [], []
    if user_day < 7:
        airplan_live = pd.read_csv('airplan/trip_airplan_%s_%s_%s.csv' % (user_day, airplan_dic[user_depart], airplan_dic[user_arrived]))
        print(airplan_live.shape)
        low_price = airplan_live.loc[airplan_live['price'] == airplan_live['price'].min()].index
        for i in low_price:
            #     print(i)
            air_type = airplan_live.loc[i][0]
            air_time = airplan_live.loc[i][1]
            air_price = airplan_live.loc[i][2]
            air_type_result.append(air_type)
            air_time_result.append(air_time)
            air_price_result.append(str(air_price))
        print(air_type_result, air_time_result, air_price_result)
    else:
        air_type_result.append('blank')
        air_time_result.append('blank')
        air_price_result.append('blank')

    resp = {
        'version': "2.0",
        "resultCode": "OK",
        "output": {
            "air_time_7": air_time_result[0],
            "air_type_7": air_type_result[0],
            "air_price_7": air_price_result[0],
        }
    }
    return json.dumps(resp, ensure_ascii=False, indent=4)


def want_weekday_airplan(req,depart,arrived,weekday):
    user_depart = depart  # 유저가 출발할 도시
    user_arrived = arrived  # 유저가 도착할 도시
    user_day = weekday  # 유저가 알고싶은 요일
    airplan_dic = {'월요일날': 0, '화요일날': 1, '수요일날': 2, '목요일날': 3, '금요일날': 4, '토요일날': 5, '일요일날': 6}
    live_day = datetime.datetime.now()
    live_day = live_day.weekday()
    want_week = airplan_dic[user_day]
    if want_week >= live_day:
        want_day = want_week - live_day
        print(want_day)
    else:
        want_day = 7 + want_week - live_day
        print(want_day)
    airplan_dic = {'서울': 0, '부산': 1, '제주': 2}
    air_type_result, air_time_result, air_price_result = [], [], []
    airplan_live = pd.read_csv('airplan/trip_airplan_%s_%s_%s.csv' % (want_day, airplan_dic[user_depart], airplan_dic[user_arrived]))
    print(airplan_live.shape)
    low_price = airplan_live.loc[airplan_live['price'] == airplan_live['price'].min()].index
    for i in low_price:
        #     print(i)
        air_type = airplan_live.loc[i][0]
        air_time = airplan_live.loc[i][1]
        air_price = airplan_live.loc[i][2]
        air_type_result.append(air_type)
        air_time_result.append(air_time)
        air_price_result.append(str(air_price))

    resp = {
        'version': "2.0",
        "resultCode": "OK",
        "output": {
            "air_time_8": air_time_result[0],
            "air_type_8": air_type_result[0],
            "air_price_8": air_price_result[0],
        }
    }
    return json.dumps(resp, ensure_ascii=False, indent=4)

def live_train_info(req,user1,arrived1):
    user = name_box_kor_fix_dic[user1]  # 누구 사용자가 출발할 도시 이름
    arrived = name_box_kor_fix_dic[arrived1]  # 누구 사용자가 도착할 도시 이름
    print('출발지',user)
    print('도착지',arrived)
    name_box_kor_dic[user]  # 사전으로 한국어를 숫자 번호를 받게 한다
    name_box_kor_dic[arrived]  # 사전으로 한국어를 숫자 번호를 받게한다 배열의 인덱스 번호로 받기 위해서
    result = []  # 시간 결과값을 담을 공간
    result_type = []  # 기차 유형에대해서 담으 공간

    # 사용자가 호출할때 실행될 실시간 시간 정보
    real_time = datetime.datetime.now()
    real_hour, real_minute = real_time.hour, real_time.minute
    real_total = real_hour * 60 + real_minute

    # 사용자가 원하는 데이터 파일 읽기
    train = pd.read_csv("train/today/SRT_%s.csv" % (name_box[name_box_kor_dic[user] - 1]))
    train_time = pd.read_csv("train/today/SRT_time_%s.csv" % (name_box[name_box_kor_dic[user] - 1]))
    train_type = pd.read_csv("train/today/SRT_type_%s.csv" % (name_box[name_box_kor_dic[user] - 1]))

    # 시간이 현재시간보다 큰 조건을 거르고
    consider = train_time[
        [name_box[name_box_kor_dic[arrived] - 1] + '_h', name_box[name_box_kor_dic[arrived] - 1] + '_m']]
    # 시간을 걸렷으면 거기서 분도 걸러서 조건에 맞는 시간을 가져온다
    consider['new_' + name_box[name_box_kor_dic[arrived] - 1]] = consider[name_box[name_box_kor_dic[arrived] - 1] + '_h'] * 60 + consider[name_box[name_box_kor_dic[arrived] - 1] + '_m']

    # 두개의 조건이 맞으면 그 조건에 맞는 첫번째 인덱스 번호를 가져온다
    try:
        find_index_number = consider[consider['new_'+name_box[name_box_kor_dic[arrived]-1]]>=real_total].index[0]
        # 인덱스 번호에 가져올 3개의 리스트 번호를 더해 변수에 담고 리스트에 저장한다
        length, _ = train.shape
        length = length - 1
        if find_index_number == length:
            find_text = train.loc[train[name_box[name_box_kor_dic[arrived]]].index[i]][name_box_kor_dic[arrived] - 1]
            find_type = train_type.loc[train_type[name_box[name_box_kor_dic[arrived]]].index[i]][
                name_box_kor_dic[arrived] - 1]
            result_type.append(find_type)
            result.append(find_text)
        elif find_index_number == length - 1:
            for i in range(find_index_number, find_index_number + 2):
                find_text = train.loc[train[name_box[name_box_kor_dic[arrived]]].index[i]][
                    name_box_kor_dic[arrived] - 1]
                find_type = train_type.loc[train_type[name_box[name_box_kor_dic[arrived]]].index[i]][
                    name_box_kor_dic[arrived] - 1]
                result_type.append(find_type)
                result.append(find_text)
        else:
            for i in range(find_index_number, find_index_number + 3):
                find_text = train.loc[train[name_box[name_box_kor_dic[arrived]]].index[i]][
                    name_box_kor_dic[arrived] - 1]
                find_type = train_type.loc[train_type[name_box[name_box_kor_dic[arrived]]].index[i]][
                    name_box_kor_dic[arrived] - 1]
                result_type.append(find_type)
                result.append(find_text)
    except IndexError:
        result = 'None','None','None'
        result_type = 'None','None','None'


    print('result : ',result)
    print('result : ',result_type)

    resp = {
        'version':"2.0",
        "resultCode":"OK",
        "output":{
            "time_1":result[0],
            "time_2":result[1],
            "time_3":result[2],
            "type_1":result_type[0],
            "type_2":result_type[1],
            "type_3":result_type[2]
        }
    }
    return json.dumps(resp,ensure_ascii=False,indent=4)


def day_train_info(req,user1,arrived1,date_time,date_time_hour,date_when):
    user = name_box_kor_fix_dic[user1]  # 누구 사용자가 출발할 도시 이름
    arrived = name_box_kor_fix_dic[arrived1]  # 누구 사용자가 도착할 도시 이름
    print('출발지', user)
    print('도착지', arrived)
    name_box_kor_dic[user]  # 사전으로 한국어를 숫자 번호를 받게 한다
    name_box_kor_dic[arrived]  # 사전으로 한국어를 숫자 번호를 받게한다 배열의 인덱스 번호로 받기 위해서
    result = []  # 시간 결과값을 담을 공간
    result_type = []  # 기차 유형에대해서 담으 공간
    # 사용자가 오후라고 하면 12를 더해서 시간을 구한다
    if date_when == '오후':
        real_time = int(date_time_hour)+12
    else:
        real_time = int(date_time_hour)
    # 내일 오늘 모래 정보 가져와서 변수에 저장 >> 엑셀 파일 읽을때 사용
    date_time_name = date_time_dic[date_time]
    date_kor_time_name = date_time_kor_dic[date_time_name]
    # 사용자가 호출할때 실행될 실시간 시간 정보
    real_hour, real_minute = real_time, 0

    # 사용자가 원하는 데이터 파일 읽기

    train = pd.read_csv("train/%s/SRT_%s.csv" % (date_time_name, name_box[name_box_kor_dic[user] - 1]))
    train_time = pd.read_csv("train/%s/SRT_time_%s.csv" % (date_time_name, name_box[name_box_kor_dic[user] - 1]))
    train_type = pd.read_csv("train/%s/SRT_type_%s.csv" % (date_time_name, name_box[name_box_kor_dic[user] - 1]))

    # 시간이 현재시간보다 큰 조건을 거르고
    consider = train_time[
        [name_box[name_box_kor_dic[arrived] - 1] + '_h', name_box[name_box_kor_dic[arrived] - 1] + '_m']]
    # 시간을 걸렷으면 거기서 분도 걸러서 조건에 맞는 시간을 가져온다
    consider = consider[(consider[name_box[name_box_kor_dic[arrived] - 1] + '_h'] >= real_hour)]
    # 두개의 조건이 맞으면 그 조건에 맞는 첫번째 인덱스 번호를 가져온다
    try:
        find_index_number = consider[(consider[name_box[name_box_kor_dic[arrived] - 1] + '_h'] >= real_hour) & (
                    consider[name_box[name_box_kor_dic[arrived] - 1] + '_m'] >= real_minute)].index[0]
        # 인덱스 번호에 가져올 3개의 리스트 번호를 더해 변수에 담고 리스트에 저장한다
        length, _ = train.shape
        length = length - 1
        if find_index_number == length:
            find_text = train.loc[train[name_box[name_box_kor_dic[arrived]]].index[i]][name_box_kor_dic[arrived] - 1]
            find_type = train_type.loc[train_type[name_box[name_box_kor_dic[arrived]]].index[i]][
                name_box_kor_dic[arrived] - 1]
            result_type.append(find_type)
            result.append(find_text)
        elif find_index_number == length - 1:
            for i in range(find_index_number, find_index_number + 2):
                find_text = train.loc[train[name_box[name_box_kor_dic[arrived]]].index[i]][
                    name_box_kor_dic[arrived] - 1]
                find_type = train_type.loc[train_type[name_box[name_box_kor_dic[arrived]]].index[i]][
                    name_box_kor_dic[arrived] - 1]
                result_type.append(find_type)
                result.append(find_text)
        else:
            for i in range(find_index_number, find_index_number + 3):
                find_text = train.loc[train[name_box[name_box_kor_dic[arrived]]].index[i]][
                    name_box_kor_dic[arrived] - 1]
                find_type = train_type.loc[train_type[name_box[name_box_kor_dic[arrived]]].index[i]][
                    name_box_kor_dic[arrived] - 1]
                result_type.append(find_type)
                result.append(find_text)
    except IndexError:
        result = 'None', 'None', 'None'
        result_type = 'None', 'None', 'None'

    print('result : ', result)
    print('result : ', result_type)

    resp = {
            'version': "2.0",
            "resultCode": "OK",
            "output": {
                "time_4": result[0],
                "time_5": result[1],
                "time_6":result[2],
                "type_4": result_type[0],
                "type_5": result_type[1],
                "type_6": result_type[2],
                "when_1":date_kor_time_name,
            }
        }
    return json.dumps(resp, ensure_ascii=False, indent=4)



@app.route('/',methods=['GET','POST'])
def hellow():
    return 'OK'

@app.route('/train_info/replay_air_want_day',methods=['GET','POST'])
@app.route('/train_info/airplan_want_day',methods=['GET','POST'])
@app.route('/train_info/airplan_want_day_lowprice',methods=['GET','POST'])
@app.route('/train_info/airplan_want_weekday',methods=['GET','POST'])
@app.route('/train_info/replay_airplan_info',methods=['GET','POST'])
@app.route('/train_info/airplan_info',methods=['GET','POST'])
@app.route('/train_info/train_want_day',methods=['GET','POST'])
@app.route('/train_info/train_info',methods=['GET','POST'])
@app.route('/train_info/more_want_info',methods=['GET','POST'])
@app.route('/train_info/train_want_more_day',methods=['GET','POST'])
def main():
    req = request.json
    print(request.json)
    print(111111111)
    action = req['action']
    print(action)
    params = action['parameters']
    print('######'*4)
    print(params)
    actionName = action['actionName']
    print('actionName :',actionName)
    print(2222222222)
    if actionName == 'train_info':
        print('성공')
        depart=params['train_depart']
        depart = depart['value']
        print('depart : ',depart)
        arrived = params['train_arrived']
        arrived = arrived['value']
        print('arrived : ',arrived)
        print('파라미터 값 확인')
        return live_train_info(req,depart,arrived)
    elif actionName == 'train_want_day':
        print('두번쨰 성공')
        depart = params['train_want_depart']
        depart = depart['value']
        print('depart : ',depart)
        arrived = params['train_want_arrived']
        arrived = arrived['value']
        print('arrived : ', arrived)
        date = params['train_date']
        date = date['value']
        print('date : ',date)
        hour = params['train_hour']
        hour = hour['value']
        print('hour : ',hour)
        when = params['train_when']
        when = when['value']
        print('when :',when)
        print('파라미터값 확인')
        return day_train_info(req,depart,arrived,date,hour,when)
    elif action == "train_want_more_day":
        print('입성')
        when = params['train_when']
        when = when['value']
        type = params['type_6']
        type = type['value']
        time = params['time_6']
        time = time['value']
        print(when,type,time)
        resp = {
                'version': "2.0",
                "resultCode": "OK",
                "output": {
                    "time_6": time,
                    "type_6": type,
                    "when_1": when,
                }
            }
        text = json.dumps(resp, ensure_ascii=False, indent=4)
        return text

    elif actionName == 'airplan_info':
        print('두번쨰 성공')
        depart = params['airplan_depart']
        depart = depart['value']
        print('depart : ',depart)
        arrived = params['airplan_arrived']
        arrived = arrived['value']
        print('arrived : ', arrived)
        print('파라미터값 확인')
        return live_airplan_info(req,depart,arrived)

    elif actionName == 'airplan_want_day':
        print('두번쨰 성공')
        depart = params['airplan_depart1']
        depart = depart['value']
        print('depart : ',depart)
        arrived = params['airplan_arrived1']
        arrived = arrived['value']
        print('arrived : ', arrived)
        hour = params['airplan_hour']
        hour = hour['value']
        print('hour : ',hour)
        when = params['airplan_when']
        when = when['value']
        print('when :',when)
        print('파라미터값 확인')
        return want_airplan_day(req,depart,arrived,when,hour)

    elif actionName == 'airplan_want_day_lowprice':
        print('두번쨰 성공')
        depart = params['airplan_depart3']
        depart = depart['value']
        print('depart : ',depart)
        arrived = params['airplan_arrived3']
        arrived = arrived['value']
        print('arrived : ', arrived)
        date = params['want_dayes']
        date = date['value']
        print('date : ',date)
        print('파라미터값 확인')
        return want_day_airplan_lowprice(req,depart,arrived,date)

    elif actionName == 'airplan_want_weekday':
        print('두번쨰 성공')
        depart = params['airplan_depart2']
        depart = depart['value']
        print('depart : ',depart)
        arrived = params['airplan_arrived2']
        arrived = arrived['value']
        print('arrived : ', arrived)
        weekdays = params['airplan_weekday']
        weekdays = weekdays['value']
        print('파라미터값 확인')
        return want_weekday_airplan(req,depart,arrived,weekdays)

    else:
        print('실행 안됨')
        if action['actionName'] == "train_want_more_day":
            print('입성')
            when = params['train_when']
            when = when['value']
            type = params['type_6']
            type = type['value']
            time = params['time_6']
            time = time['value']
            print(when, type, time)
            resp = {
            'version': "2.0",
            "resultCode": "OK",
            "output": {
                "time_6": time,
                "type_6": type,
                "when_1": when,
                    }
             }
            text = json.dumps(resp, ensure_ascii=False, indent=4)
            return text
        elif action['actionName'] == "more_want_info":
            print('입성')
            type = params['type_3']
            type = type['value']
            time = params['time_3']
            time = time['value']
            print( type, time)
            resp = {
            'version': "2.0",
            "resultCode": "OK",
            "output":
            {
                "time_3": time,
                "type_3": type,
               }
             }
            text = json.dumps(resp, ensure_ascii=False, indent=4)
            return text
        elif action['actionName'] == "replay_airplan_info":
            print('입성')
            type = params['air_type_3']
            type = type['value']
            time = params['air_time_3']
            time = time['value']
            price = params['air_price_3']
            price = price['value']
            print(price,type, time)
            resp = {
            'version': "2.0",
            "resultCode": "OK",
            "output":
            {
                "air_time_3": time,
                "air_type_3": type,
                'air_price_3' : price
               }
             }
            text = json.dumps(resp, ensure_ascii=False, indent=4)
            return text

        elif action['actionName'] == "replay_air_want_day":
            print('입성')
            type = params['air_type_6']
            type = type['value']
            time = params['air_time_6']
            time = time['value']
            price = params['air_price_6']
            price = price['value']
            print(price,type, time)
            resp = {
            'version': "2.0",
            "resultCode": "OK",
            "output":
            {
                "air_time_6": time,
                "air_type_6": type,
                'air_price_6' : price
               }
             }
            text = json.dumps(resp, ensure_ascii=False, indent=4)
            return text
        print('진짜 안됨')


        print('진짜 안됨')
        return ''

if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
