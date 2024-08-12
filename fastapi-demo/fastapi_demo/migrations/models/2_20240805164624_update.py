from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `basemodel` DROP COLUMN `create_time`;
        ALTER TABLE `basemodel` DROP COLUMN `update_time`;
        ALTER TABLE `chatrecord` DROP COLUMN `create_time`;
        ALTER TABLE `chatrecord` DROP COLUMN `update_time`;
        ALTER TABLE `multestmodel` DROP COLUMN `create_time`;
        ALTER TABLE `multestmodel` DROP COLUMN `update_time`;
        ALTER TABLE `user` DROP COLUMN `create_time`;
        ALTER TABLE `user` DROP COLUMN `update_time`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD `create_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `user` ADD `update_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `basemodel` ADD `create_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `basemodel` ADD `update_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `chatrecord` ADD `create_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `chatrecord` ADD `update_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `multestmodel` ADD `create_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `multestmodel` ADD `update_time` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);"""
