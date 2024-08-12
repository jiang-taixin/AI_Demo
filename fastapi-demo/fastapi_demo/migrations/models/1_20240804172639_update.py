from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `multestmodel` ADD `comment` VARCHAR(255) NOT NULL  COMMENT '备注' DEFAULT '';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `multestmodel` DROP COLUMN `comment`;"""
