# StudyWatson API

## API 설명

### Authentication

사용자 인증이 필요한 경우, Token인증을 사용합니다. Token인증에는 아래 라이브러리를 사용하고 있습니다.  
[DRF Authentication - Token](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)



#### Token획득법

[API Docs - AuthToken](<https://fitcha.lhy.kr/doc/#operation/auth_token_create>)
`/auth/token/` URL에 아래와 같은 데이터를 `POST` 방식으로 전송

```json
{
  "username": "string",
  "password": "string"
}
```

성공시 Token문자열과 User를 객체로 리턴

```json
{
    "key": "a129b636dc3f352f864398b471f17b43bb4ce352",
    "user": {
        "attr": "value"
    }
}
```



#### Token 사용법

```
Authorization: Token a129b636dc3f352f864398b471f17b43bb4ce352
```

위 key/value를 HTTP Request header로 지정해서 전송 (value의 token값 앞에 "Token "문자열이 존재해야 함)
