# CUE 자동 포스팅 봇

인스타그램 @__cuemag 계정에 하루 3번(한국시간 9시/15시/21시) 자동으로
주제 선정 → 캡션 작성 → 포스터 제작 → 게시까지 자동으로 해주는 봇입니다.

## 처음 설정하는 방법 (딱 한 번만 하면 됨)

### 1. GitHub에 새 저장소 만들기
1. github.com 로그인 → 우측 상단 **+** → **New repository**
2. Repository name: `cue-bot` (원하는 이름으로 해도 됨)
3. **Public**으로 설정 (이미지가 공개 URL로 접근 가능해야 하기 때문에 반드시 Public)
4. **Create repository** 클릭

### 2. 이 파일들을 저장소에 업로드
1. 방금 만든 저장소 페이지에서 **Add file → Upload files** 클릭
2. 이 프로젝트 폴더 안의 모든 파일/폴더를 그대로 드래그 앤 드롭
   (`.github` 폴더가 포함되어 있는지 꼭 확인하세요 — 안 보이면 숨김 폴더라 그럴 수 있으니, 압축(zip)해서 올린 뒤 GitHub에서 압축 해제되는지 확인하거나, 폴더째로 드래그해보세요)
3. **Commit changes** 클릭

### 3. 비밀 키(Secrets) 등록
저장소 페이지 → **Settings** → 좌측 메뉴 **Secrets and variables → Actions** → **New repository secret**

아래 5개를 하나씩 등록하세요 (이름은 정확히 똑같이 입력):

| Secret 이름 | 값 |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic 콘솔에서 발급받은 키 |
| `OPENAI_API_KEY` | OpenAI 플랫폼에서 발급받은 키 |
| `IG_USER_ID` | `17841479914962366` |
| `IG_ACCESS_TOKEN` | Meta 개발자 사이트에서 발급받은 Instagram 액세스 토큰 |

### 4. Actions 켜기
저장소 페이지 → **Actions** 탭 클릭 → "I understand my workflows, go ahead and enable them" 같은 버튼이 있으면 클릭해서 활성화

### 5. 테스트로 한 번 실행해보기
1. **Actions** 탭 → 좌측에서 **CUE 자동 포스팅** 클릭
2. 우측 **Run workflow** 버튼 클릭 → 다시 **Run workflow** 확인 클릭
3. 1~2분 후 인스타그램 @__cuemag 계정에 실제로 게시되는지 확인!

## 이후에는?
따로 뭘 안 하셔도 매일 한국시간 9시/15시/21시에 자동으로 실행됩니다.
실행 기록은 저장소의 **Actions** 탭에서 항상 확인할 수 있어요.

## 유지보수 관련 참고사항
- Instagram 액세스 토큰은 보통 60일 정도 후 만료돼요. 게시가 갑자기 실패하기 시작하면,
  Meta 개발자 사이트에서 토큰을 다시 발급받아 `IG_ACCESS_TOKEN` Secret 값을 갱신해주세요.
- 이미지/텍스트 생성 API는 사용한 만큼 비용이 청구되니, 가끔 Anthropic/OpenAI 콘솔에서
  잔여 크레딧을 확인해주세요.
