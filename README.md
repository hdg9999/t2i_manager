T2I Manager
(Text to Image Manager)
==================================

개요
---
개인 PC에 저장된 이미지가 매우 많아서 본인도 어떤 사진이 어디에 있는지 찾기 힘든 경우를 대비하여 사진 파일을 임베딩으로 저장하고, 자연어로 검색할 수 있게 도와주는 프로그램입니다. 이와 더불어 있는지 없는지도 잘 모르겠는 Windows 탐색기의 기본 태깅보다 더 나은 ~~(것 같다고 나만 생각하는)~~ 태깅 기능도 지원하므로 임베딩과 태그를 활용해 당신의 소중한 사진들을 관리해보세요.

사진이 

설치 및 실행방법
---
실행 환경은 Windows 기준입니다.   
Mac에서는 tkinter를 별도 설치하면 될 수도 있으나 직접 테스트해보지 않아서 실행여부를 보장하지 않습니다. 

파이썬 설치 및 가상환경 세팅 등은 생략합니다.

1. 필수 의존성 설치
```
pip install -r requirements.txt
```   
2. 실행
```
streamlit run app.py
```   
- 포트 변경 등 실행 옵션을 변경하고 싶은 경우에는 streamlit 공식 문서에 따라 실행 인수를 뒤에다가 작성하세요.
- 실행 옵션과 관련해서는 [streamlit 공식 문서 - streamlit run](https://docs.streamlit.io/develop/api-reference/cli/run) 을 참고하세요.   



3. 접속
    
- 브라우저를 통해 실행 명령어 실행 후 나타나는 url로 접속합니다.
- 기본설정으로 실행한 경우 자동으로 http://localhost:8501 로 브라우저가 켜지나, 사용하시는 PC 환경에 따라 포트번호가 다르거나 할 수 있습니다.

기본 사용방법
---

### 사진 등록
1. 폴더 등록 페이지로 이동하여 폴더 선택 버튼을 누릅니다.
2. 폴더 선택창이 나타나면 업로드할 사진들이 저장된 폴더를 선택합니다.
3. 폴더 등록 버튼을 눌러서 업로드합니다. (폴더 내 jpg, png, gif, webp 파일만 업로드 됩니다.)
4. Home 페이지로 돌아와서 검색합니다.

### 태그 관리 및 사진에 태그 지정
1. 좌측 메뉴 바의 태그 추가 입력란에 추가하고자 하는 태그를 입력합니다.
2. 태그추가 버튼을 눌러 저장합니다.
3. Home 페이지에서 이미지를 검색합니다.
4. 태그를 지정하고 싶은 사진 아래의 버튼을 눌러 이미지 상세 팝업을 띄웁니다.
5. 하단의 태그 란에 추가하고 싶은 태그를 찾아 선택 후 변경사항 저장 버튼을 클릭합니다.

DB 초기화 방법
---
버그/오류 때문에 어쩔 수 없이 데이터 초기화를 하고자 하는 경우에는 프로그램 종료 후 소스 경로의 chroma 폴더 내 파일을 모두 삭제하고 다시 폴더 등록을 진행하시면 됩니다.
