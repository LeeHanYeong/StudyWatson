from typing import NamedTuple


class Error(NamedTuple):
    code: str
    message: str
    case: str


# Common
UNDEFINED = Error(
    'undefined',
    '정의되지 않은 오류',
    '정의되지 않은 경우',
)

# UserCreate
EMAIL_SEND_FAILED = Error(
    'emailSendFailed',
    '인증 이메일 발송에 실패했습니다',
    '인증 이메일 발송에 실패한 경우',
)
EMAIL_VERIFICATION_INCOMPLETED = Error(
    'emailVerificationIncompleted',
    '이메일 인증이 완료되지 않았습니다. 메일을 확인해주세요',
    '이메일 인증이 완료되지 않은 경우',
)
EMAIL_VERIFICATION_NOT_EXISTS = Error(
    'emailVerificationNotExists',
    '이메일 인증정보가 없습니다',
    '이메일 인증정보가 없는 경우',
)

# Study
STUDY_INVITE_TOKEN_INVALID = Error(
    'studyInviteTokenInvalid',
    '스터디 초대 토큰이 유효하지 않습니다',
    '스터디 초대 토큰이 유효하지 않거나 존재하지 않는 경우',
)

# StudyMembership
MEMBERSHIP_ALREADY_EXISTS = Error(
    'membershipAlreadyExists',
    '스터디멤버십이 이미 존재합니다',
    '스터디멤버십이 이미 존재할 경우',
)
