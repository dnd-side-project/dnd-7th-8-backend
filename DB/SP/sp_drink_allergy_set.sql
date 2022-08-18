CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_drink_allergy_set` (
     IN `i_drink_id`        INTEGER
    ,IN `i_allergy`         VARCHAR(255)
    ,OUT `o_out_code`       SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_drink_allergy_set : 음료 알레르기 데이터 인서트
author : dylee
RELEASE : 0.0.1
LAST UPDATE : 2022-08-15
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

    -- 1. 데이터 인서트
    INSERT INTO drink_tag(
         `drink_id`
        ,`allergy`
    ) VALUES(
         `i_drink_id`
        ,`i_allergy`
    );

    COMMIT;

END