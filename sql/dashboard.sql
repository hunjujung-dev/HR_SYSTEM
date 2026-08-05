-- Dashboard 테스트용 공지사항 테이블
IF OBJECT_ID('TB_NOTICE') IS NULL
BEGIN
    CREATE TABLE TB_NOTICE(
        NOTICE_ID INT IDENTITY(1,1) PRIMARY KEY,
        TITLE NVARCHAR(200),
        CONTENT NVARCHAR(MAX),
        NOTICE_DATE DATETIME DEFAULT GETDATE()
    )
END

-- 샘플 데이터
INSERT INTO TB_NOTICE(TITLE,CONTENT)
VALUES
('근태 정책 변경 안내','7월부터 지각 기준이 변경됩니다.'),
('시스템 점검 안내','주말 점검 예정입니다.'),
('휴가 신청 기간 안내','하계 휴가 신청 바랍니다.');