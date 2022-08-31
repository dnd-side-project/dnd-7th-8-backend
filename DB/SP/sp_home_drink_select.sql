CREATE DEFINER=`dylee`@`%` PROCEDURE `sp_home_drink_select` (
     IN  `i_limit`       INT
    ,OUT `o_out_code`         SMALLINT
)

BEGIN
/* ----------------------------------------------------------------------------
sp_home_drink_select : 인기 레시피 조회
author : dylee
RELEASE : 0.0.1
LAST UPDATE : 2022-08-26
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

      -- 3. 
      SELECT D.drink_id
           , D.drink_name
           , D.img
           , D.price
           , IFNULL((SELECT GROUP_CONCAT(tag) FROM drink_tag WHERE drink_id=D.`drink_id`),'') as `tag`
           , (SELECT COUNT(*) FROM drink_like WHERE drink_id = D.`drink_id`) as `like_cnt`
      FROM drink as D
      ORDER BY drink_id ASC
      LIMIT i_limit;

END