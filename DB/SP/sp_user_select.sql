CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_user_by_email_select` (
     IN `i_email`         VARCHAR(255)     -- 이메일
    ,IN `i_platform`      ENUM('not_social', 'kakao')
    ,OUT `o_out_code`     SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_user_by_email_select : 이메일 정보로 유저 조회
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


    -- 1. email 정보로 유저 정보 조회
    SELECT `customer_uuid`
         , `email`
         , `nickname`
         , `passwd`
         , `birth`
         , `profile`
    FROM mazle_user
    WHERE email = i_email
      AND platform = i_platform;
    

END