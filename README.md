# post-list-page

## Requirements

- Python 3
- Pipenv

## Setup

1. **Dependencies 설치**

   먼저 필요한 패키지들을 설치하기 위해 다음의 명령어를 실행합니다:

   ```bash
   pipenv install
   ```

2. **기본 프로젝트 setup**

   ```
   make setup
   ```

3. **서버 실행**

   ```bash
   make run
   ```

   외에 나머지 필요한 명령어는 Makefile에서 확인할 수 있습니다.

---

인증관련 기능 구현이 필요하지 않아서, 로그인 없이 슈퍼유저 계정으로만 게시글이 등록됩니다.

## API

게시물 목록 실제 페이지는 다음과 같습니다.

```
http://localhost:8000/posts/
```

drf API 는 다음과 같습니다.

```
http://localhost:8000/api/posts
```

admin 페이지는 다음과 같습니다.

```
http://localhost:8000/admin
```
