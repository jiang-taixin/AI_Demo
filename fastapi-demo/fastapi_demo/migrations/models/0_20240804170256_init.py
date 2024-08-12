from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `basemodel` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8;
CREATE TABLE IF NOT EXISTS `multestmodel` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `create_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(255) NOT NULL  COMMENT '名称'
) CHARACTER SET utf8;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    `create_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `user_name` VARCHAR(32) NOT NULL  COMMENT '用户名',
    `password` VARCHAR(32) NOT NULL  COMMENT '密码',
    `telephone` VARCHAR(15) NOT NULL  COMMENT '手机号'
) CHARACTER SET utf8;
CREATE TABLE IF NOT EXISTS `chatrecord` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '对话ID',
    `create_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `request_id` VARCHAR(40) NOT NULL  COMMENT ' 请求ID',
    `input_tokens` INT NOT NULL  COMMENT 'Input Tokens',
    `output_tokens` INT NOT NULL  COMMENT 'Output Tokens',
    `total_tokens` INT NOT NULL  COMMENT 'Total Tokens',
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_chatreco_user_e4b10542` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8;
CREATE TABLE IF NOT EXISTS `chatrecord_multestmodel` (
    `chatrecord_id` INT NOT NULL,
    `multestmodel_id` INT NOT NULL,
    FOREIGN KEY (`chatrecord_id`) REFERENCES `chatrecord` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`multestmodel_id`) REFERENCES `multestmodel` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_chatrecord__chatrec_9d6e09` (`chatrecord_id`, `multestmodel_id`)
) CHARACTER SET utf8 COMMENT='测试多对多';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
