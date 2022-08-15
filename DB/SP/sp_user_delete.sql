CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_user_signup_set` (
     IN `i_customer_uuid`   VARCHAR(255)     -- 유저 고유 ID
    ,OUT `o_out_code`       SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_user_signup_set : 회원 탈퇴 SP - 추후 DELETE가 아닌 flag값 변경하는것으로 변경 예정
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


    -- 1. 유저 정보 삭제(추후 flag값 변경으로 변경 예정)
    DELETE mazle_user
    


END