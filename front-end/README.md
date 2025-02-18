# 🚀 FinPilot - Frontend

FinPilot은 Google Docs에서 금융 문서 작성 및 편집을 위한 AI 도우미로 LLM(sLLM) 기반 초안 작성, 단락 생성, 요약 및 확장과 데이터 시각화를 지원합니다.

**Frontend**는 사용자가 직관적으로 접근할 수 있는 사용자 인터페이스를 제공하며, 이를 활용하여 금융 문서 생성 및 편집을 돕습니다.

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Features](#-features)
- [File Structure](#-file-structure)
- [Tech Stack](#-tech-stack)
- [Communication](#-communication)
- [Setup and Installation](#%EF%B8%8F-setup-and-installation)
- [How to Run](#-how-to-run)
- [Contribution](#-contribution)
- [Contact](#-contact)

---

## 📋 About the Project

FinPilot은 **Google Docs**에서 금융 문서를 보다 쉽게 작성하고 편집할 수 있도록 도와주는 LLM 기반 **Chrome 확장 프로그램**입니다.
실시간 초안 작성, 단락 생성, 요약 및 확장과 데이터 시각화 등 금융 전문가와 비즈니스 사용자에게 최적화된 기능을 제공합니다.

---

## ✨ Features

- **AI-Driven Chatbot**: 사용자의 입력에 따라 AI가 실시간으로 텍스트를 생성.
- **Google Docs Integration**: 생성된 텍스트를 Google Docs에 바로 반영 가능.
- **Responsive Design**: 반응형 디자인으로 다양한 화면 크기에서도 완벽히 작동.
- **Authentication**: Google 로그인 기능 제공.
- **User-Friendly Interface**: 간결하고 직관적인 Sidebar UI.

---

## 🗂 File Structure

```
front-end/                     # Frontend 폴더
├── README.md                  # 프로젝트 설명 파일
├── FinPilot/                  # Chrome 확장 프로그램 폴더
│   ├── .gitignore             # Git에서 제외할 파일 목록
│   ├── Advice.png             # 조언 아이콘
│   ├── Analysis.png           # 분석 관련 아이콘
│   ├── apply.png              # 'Apply' 버튼 아이콘
│   ├── background.js          # 백그라운드 스크립트
│   ├── chat_option_1.png      # 채팅 옵션 1 아이콘
│   ├── chat_option_2.png      # 채팅 옵션 2 아이콘
│   ├── chat_option_3.png      # 채팅 옵션 3 아이콘
│   ├── chat_option_4.png      # 채팅 옵션 4 아이콘
│   ├── chat_option_5.png      # 채팅 옵션 5 아이콘
│   ├── check-icon.png         # 체크 아이콘
│   ├── copy.png               # 복사 버튼 아이콘
│   ├── copy_done.png          # 복사 완료 아이콘
│   ├── credit.png             # 신용카드 관련 아이콘
│   ├── default_profile.webp   # 기본 프로필 이미지
│   ├── diversified_investment.png # 분산 투자 관련 아이콘
│   ├── down_graph.png         # 하락 그래프 아이콘
│   ├── file_upload.png        # 파일 업로드 버튼 아이콘
│   ├── guide.gif              # 팝업창 가이드 GIF
│   ├── icon_128.png           # 128px 크기의 앱 아이콘
│   ├── icon_16.png            # 16px 크기의 앱 아이콘
│   ├── icon_32.png            # 32px 크기의 앱 아이콘
│   ├── icon_48.png            # 48px 크기의 앱 아이콘
│   ├── icon_64.png            # 64px 크기의 앱 아이콘
│   ├── icon_circle.png        # 원형 아이콘
│   ├── link.png               # 링크 아이콘
│   ├── manifest.json          # Chrome 확장 프로그램 설정 파일
│   ├── marked.min.js          # 마크다운 파싱 라이브러리
│   ├── money.png              # 금융 관련 아이콘
│   ├── money_hand.png         # 돈을 들고 있는 손 아이콘
│   ├── package-lock.json      # 패키지 종속성 파일
│   ├── package.json           # 패키지 설정 파일
│   ├── popup.css              # 팝업창 스타일
│   ├── popup.html             # 팝업창 페이지
│   ├── popup.js               # 팝업창 스크립트
│   ├── privacy-policy.md      # FinPilot 개인정보 보호 정책
│   ├── rebalancing.png        # 포트폴리오 리밸런싱 아이콘
│   ├── sad.png                # 슬픈 표정 아이콘
│   ├── send_icon.png          # 전송 버튼 아이콘
│   ├── sidebar.html           # 사이드바 HTML
│   ├── sidebar.js             # 사이드바 기능 구현
│   ├── source.png             # 출처 버튼 아이콘
│   ├── source_h3.png          # 출처 헤더 이미지
│   ├── style.css              # 사이드바 스타일 시트
│   ├── up_graph.png           # 상승 그래프 아이콘
│   ├── web/                   # 웹 관련 페이지 폴더
│   │   ├── info/              # 채팅 옵션 info 페이지 폴더
│   │   │   ├── info.css       # info 페이지 스타일
│   │   │   ├── info.html      # info 페이지 HTML
│   │   │   ├── upload_1.png   # 업로드 기반 그래프 이미지 1
│   │   │   ├── upload_2.png   # 업로드 기반 그래프 이미지 2
│   │   │   ├── web_graph.png  # 웹 그래프 이미지
│   │   ├── landing/           # 랜딩 페이지 폴더
│   │   │   ├── landing.html   # 랜딩 페이지 HTML
│   │   │   ├── landing_files/ # 랜딩 페이지 이미지 폴더
│   │   │   │   ├── background.png  # 배경 이미지
│   │   │   │   ├── fp_gif_1.gif    # GIF 애니메이션 1
│   │   │   │   ├── fp_gif_2.gif    # GIF 애니메이션 2
│   │   │   │   ├── fp_png_1.png    # PNG 이미지 1
│   │   │   │   ├── fp_png_2.png    # PNG 이미지 2
│   │   │   │   ├── img_1.webp      # 사용자 리뷰 이미지 1 
│   │   │   │   ├── img_10.jpg      # 사용자 리뷰 이미지 10
│   │   │   │   ├── img_11.jpg      # 사용자 리뷰 이미지 11
│   │   │   │   ├── img_12.jpg      # 사용자 리뷰 이미지 12
│   │   │   │   ├── img_2.webp      # 사용자 리뷰 이미지 2
│   │   │   │   ├── img_3.webp      # 사용자 리뷰 이미지 3
│   │   │   │   ├── img_4.webp      # 사용자 리뷰 이미지 4
│   │   │   │   ├── img_5.webp      # 사용자 리뷰 이미지 5
│   │   │   │   ├── img_6.webp      # 사용자 리뷰 이미지 6
│   │   │   │   ├── img_7.webp      # 사용자 리뷰 이미지 7
│   │   │   │   ├── img_8.webp      # 사용자 리뷰 이미지 8
│   │   │   │   ├── img_9.webp      # 사용자 리뷰 이미지 9
│   │   │   │   ├── script             # JS 폴더
│   │   │   │   ├── script_main.Y4SCJLDF.mjs  # 메인 스크립트 파일
│   │   ├── login/              # 로그인 페이지 폴더
│   │   │   ├── login.css       # 로그인 페이지 스타일
│   │   │   ├── login.html      # 로그인 페이지 HTML
│   │   │   ├── login.js        # 로그인 페이지 스크립트
│   │   ├── start/              # 시작 페이지 폴더
│   │   │   ├── start.css       # 시작 페이지 스타일
│   │   │   ├── start.html      # 시작 페이지 HTML
│   │   │   ├── start.js        # 시작 페이지 스크립트
```

---

## 🛠 Tech Stack

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Google Drive API](https://img.shields.io/badge/Google%20Drive%20API-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)
![Google Docs API](https://img.shields.io/badge/Google%20Docs%20API-4285F4?style=for-the-badge&logo=google&logoColor=white)
![OpenAI GPT API](https://img.shields.io/badge/OpenAI%20API-412991?style=for-the-badge&logo=openai&logoColor=white)
![Chrome Extensions](https://img.shields.io/badge/Chrome%20Extensions-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)
![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)
![Framer](https://img.shields.io/badge/Framer-0055FF?style=for-the-badge&logo=framer&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)

---

## 📢 Communication

![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)
![Chrome Web Store](https://img.shields.io/badge/Chrome%20Web%20Store-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white)
![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)

---

## ⚙️ Setup and Installation

### Prerequisites
- Chrome 브라우저
- Google Account
- Google Docs

### Installation Steps
1. **Repository Clone**
   ```bash
   git clone https://github.com/FinPilotAI/FinPilot.git
   cd FinPilot/front-end
   ```

2. **Chrome Extension 로드**
   - Chrome의 `chrome://extensions`로 이동.
   - "Developer mode"를 활성화한 뒤 "Load unpacked"를 클릭.
   - `FinPilot` 폴더를 선택하여 확장 프로그램을 로드합니다.

---

## 🚀 How to Run

1. **Extension 실행**:
   - Chrome 브라우저에서 우측 상단 FinPilot 확장 아이콘 클릭
   - 설명에 따라서 로그인까지 진행
   - Google Docs 페이지에서 문서 열기
   - Chrome 브라우저에서 우측 상단 FinPilot 확장 아이콘 우클릭
   - 측면 패널 열기 선택

2. **AI 기능 테스트**:
   - SidePanel에서 원하는 채팅 옵션 선택 후, 질문 입력
   - 생성된 텍스트 확인
   - apply 버튼으로 생성 텍스트가 Google Docs 문서에 자동으로 반영되는지 확인
   - source 버튼으로 생성 답변의 출처 확인

---

## 🤝 Contribution

1. **Fork this repository**.
2. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Commit your changes**:
   ```bash
   git commit -m "Add new feature"
   ```

4. **Push to the branch**:
   ```bash
   git push origin feature/your-feature
   ```

5. **Open a Pull Request**.

---

## 📧 Contact

- **Email**: sjh75555@naver.com
- **GitHub**: [https://github.com/wkd-gh](https://github.com/wkd-gh)

---

> 이 README는 **FinPilot 프론트엔드 브랜치**에 최적화된 문서입니다. 

> 전체 프로젝트에 대한 자세한 내용은 Main 브랜치의 README를 참조하세요.
