# 질문과 답변으로부터 얻을 수 있는 정보를 하나의 평서문으로 추출
'''
1. 트리플 + a
(부사절, 명사절, 장소 , 시간등)
2. 인과관계 추출 -> 하나의 문장 혹은 키워드 로 만들기
3. 질의 + 대답을 통해 하나의 문장 만들기
4. 문장 쪼개기
'''
import string
import os

path = 'C:/Users/User/OneDrive/바탕 화면/2022/학부연구생/QA/'
file_list = os.listdir(path)
file_list_py = [file for file in file_list if file.startswith('CBCA')] # CBCA로 시작하는 텍스트 파일을 리스트에 저장

for files in file_list_py:
    f=open(files,"rt",encoding='UTF8') 
    # UnicodeDecodeError: 'cp949' codec can't decode byte 0xed in position 23: illegal multibyte sequence
    # -> encoding='UTF8' 추가

    linelist=[]
    print('========================================================')
    print(files)

    lines=[] # 텍스트 파일에 있는 문장(str)
    linelist=[] # 인덱스를 활용하기 위하여 문장을 리스트에 저장(list)

    #단답형만 고려(예/아니오)
    positive=[] # 답변이 "예" 또는 "네" 또는 "(고개를 끄덕이다)"로 코딩되어 있는 경우
    negative=[] # 답변이 '아니-'로 시작하는 경우

    for paragraph in f:
        lines = paragraph.split('\n')
        linelist.append(lines[0])
        # for index, value in enumerate(linelist):
        #     print(index,value)
        answer=[]
        for sent in list(enumerate(linelist)):
            sent=list(sent)
            if sent[1].startswith("답")>0:
                sent[1]=sent[1].lstrip("답")
                answer.append(sent)
            elif sent[1].startswith("피해자")>0:
                sent[1]=sent[1].lstrip("피해자")
                answer.append(sent)
            else: pass # 진술 파일마다 형식이 달라서 수정 필요
        
    for sent in answer:
        if sent[1].startswith("네")>0 or sent[1].startswith("예")>0 or sent[1].startswith("(고개를 끄덕이다)")>0:
            positive.append(sent)
            # print("긍정",sent)
        elif sent[1].startswith("아니")>0:
            negative.append(sent)
            # print("부정",sent)       
        else: pass     
    
    # print('-----------긍정-----------\n',positive)
    # print('-----------부정-----------\n',negative)

    for item in positive:
        question=linelist[(item[0]-1)]
        if question.startswith("문")>0:
            question=question.lstrip("문")
            item.insert(0,question)
        elif question.startswith("분석관")>0:
            question=question.lstrip("분석관")
            item.insert(0,question)
        else: pass        
        
    print('<<<<<<< 긍정 >>>>>>>\n',positive)   # [질문, index(몇 번째 문장인지), 답변] 형태로 출력

    for item in negative:
        question=linelist[(item[0]-1)]
        if question.startswith("문")>0:
            question=question.lstrip("문")
            item.insert(0,question)
        elif question.startswith("분석관")>0:
            question=question.lstrip("분석관")
            item.insert(0,question)
        else: pass # 진술 파일마다 형식이 달라서 수정 필요
        
    print('<<<<<<< 부정 >>>>>>>\n',negative)  

'''
[Task 1]
의문문 -> 평서문 
'예/아니오' 단답형이므로 질문의 동사 형식 & 문장 부호만 변경해도 의미 전달 가능
*영어와 달리 한국어는 의문문과 평서문의 문장 형태가 동일한 경우가 적지 않다.

(1) 답변이 긍정인 경우, 대부분의 경우 문장 부호만 변경해도 의미 전달 가능 (*구어체 유지 - 예시 1)

@예시 1 : 문장 부호만 ?->.으로 변경해도 되는 경우
잘 기억이 안나요? / 동생도 같이 있었어요? / 다른 건 없어요? 
-> 문장 부호만 .으로 변경 또는 제거
*둘 다 휴대폰 하고 있었어? / 발걸음 소리가 들렸어?

@예시 2 : 문장 부호 & 동사 형식도 변경해야 자연스러운 경우
정수기 반대편 쪽에 동생이 앉은 거네요?
-> 정수기 반대편 쪽에 동생이 앉은 거다.
뒤를 돌려고 이렇게 했었는데 그 할아버지가 가셨다는말이죠?
-> 뒤를 돌려고 이렇게 했었는데 그 할아버지가 가셨다.

(2) 답변이 부정인 경우

@예시 1: 동사 형식을 변경해야 하는 경우

평소에도 다 벗고 있었다는 건 평소에도 아예 나체를 봤었다는 얘기예요?
-> 평소에도 다 벗고 있었다는 건 평소에도 아예 나체를 봤었다는 얘기가 아니다.

엄마가 첫 번째 있었던 일만 모르는 거예요?
-> 엄마가 첫 번째 있었던 일만 모르는 거 아니다.(게 아니다/것이 아니다)

친구가 슈퍼를 해요?
-> 친구가 슈퍼를 하지 않는다.

할아버지가 들어오니까 이렇게 나갔어?
-> 할아버지가 들어오니까 이렇게 나가지 않았다.

@예시 2: 질문 형식이 다른 경우
이때 OO가 중2 되니까? 맞나?
-> 이때 OO가 중2 되는 것이 아니다

@예시 3: 습관적인 '아니' 
문: 시선이  느껴질랑말랑’이라는 말이 무슨 말인지...
답: 아니, 뭔가 보는 듯 하면서 안 보는 것 같고 뭔가 갑자기 막 사라지고 막 보고 뭐라고 해야 되지?

[Task 2]
예/아니오 외의 답변들

@예시 -> 질문을 모르면 답변의 의미/맥락을 파악하기 어려운 경우
싫었어요. 기억이 안나요.
방학.
혼날까봐.

'''