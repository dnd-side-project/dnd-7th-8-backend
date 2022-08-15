CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_user_signup_set` (
     IN `i_email`         VARCHAR(255)     -- 이메일
    ,IN `i_nickname`      VARCHAR(255)     -- 닉네임
    ,IN `i_passwd`        VARCHAR(255)     -- passwd(PasswordHasher를 통해 해싱된 pw)
    ,IN `i_birth`         DATE             -- 생년월일
    ,IN `i_profile`       LONGBLOB         -- 프로필 사진
    ,IN `i_platform`      ENUM('not_social', 'kakao')
    ,OUT `o_out_code`     SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_user_signup_set : 유저 인서트 SP
author : dylee
RELEASE : 0.0.1
LAST UPDATE : 2022-08-12
---------------------------------------------------------------------------- */ 

    DECLARE EXIT HANDLER FOR SQLEXCEPTION, NOT FOUND, SQLWARNING
    BEGIN
        GET DIAGNOSTICS CONDITION 1 @v_sql_state = RETURNED_SQLSTATE
                , @v_error_no = MYSQL_ERRNO
                , @v_error_msg = MESSAGE_TEXT;
                SELECT @v_error_msg ; 
        ROLLBACK;
        SET o_out_code = -99;
    END;

    SET o_out_code = 0;


    -- 1. customer_uuid 생성
    SET @v_customer_uuid = UUID();

    -- 2. 유저 정보 인서트
    INSERT INTO mazle_user(
         `customer_uuid`
        ,`email`
        ,`nickname`
        ,`passwd`
        ,`birth`
        ,`profile`
        ,`platform`
    ) VALUES (
         @v_customer_uuid
        ,`i_email`
        ,`i_nickname`
        ,`i_passwd`
        ,`i_birth`
        ,`i_profile`
        ,`i_platform`
    );

END