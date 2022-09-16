CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_drink_comment_set` (
     IN `i_drink_id`        VARCHAR(40)     -- 음로ID
    ,IN `i_customer_uuid`   VARCHAR(40)     -- 유저ID
    ,IN `i_comment`         VARCHAR(255)    -- 댓글
    ,IN `i_score`           FLOAT(3,1)      -- 별점
    ,OUT `o_out_code`       SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_drink_comment_set : 레시피 리뷰 등록
author : dylee
RELEASE : 0.0.1
LAST UPDATE : 2022-08-16
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

    START TRANSACTION;

    INSERT INTO drink_comment (
         `drink_id`
        ,`customer_uuid`
        ,`comment`
        ,`score`
    ) VALUES (
         `i_drink_id`
        ,`i_customer_uuid`
        ,`i_comment`
        ,`i_score`
    );

    COMMIT;

END