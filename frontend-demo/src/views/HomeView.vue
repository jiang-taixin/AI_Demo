<template>
  <a-flex vertical style="height: 100%">
    <a-flex align="baseline" justify="space-between">
      <a-flex align="baseline">
        <p>登录用户：{{userStore.userName}}</p>
        <p>用户Id：{{userStore.userId}}</p>
        <p>手机号：{{userStore.telephone}}</p>
      </a-flex>
      <a-flex align="baseline">
        <a-button @click="edit">修改信息</a-button>
        <a-button @click="logout">登出</a-button>
      </a-flex>
    </a-flex>

    <a-flex vertical align="center">
      <div class="chat-container">
        <template v-for="item in chatRecord">
          <a-row :gutter="10" v-if="item.role === 'robot'" style="margin-top: 5px; align-items: center; margin-left: 5px">
            <a-col :span="1" >
              <a-avatar>
                <template #icon><RobotOutlined /></template>
              </a-avatar>
            </a-col>
            <a-col :span="23" >
              <MdPreview :editorId="id" :modelValue="item.content" />
            </a-col>
          </a-row>
          <a-row :gutter="10" v-if="item.role === 'person'" style="margin-top: 5px; align-items: center; margin-left: 5px">
            <a-col :span="1" >
              <a-avatar>
                <template #icon><UserOutlined /></template>
              </a-avatar>
            </a-col>
            <a-col :span="23" >
              <MdPreview :editorId="id" :modelValue="item.content" />
            </a-col>
          </a-row>

        </template>
      </div>
    </a-flex>
    <a-row :gutter="10" style="margin-top: 20px">
      <a-col :span="16" :offset="2">
        <a-input @keyup.enter="chat" v-model:value="chatMessage.content" />
      </a-col>
      <a-col :span="4">
        <a-button @click="chat" style="width: 100%" :loading="loading" :disabled="loading">发送</a-button>
      </a-col>
    </a-row>

  </a-flex>
</template>
<script setup lang="ts">
import {onMounted, reactive, ref} from "vue";
import router from "@/router";
import { useUserStore } from "@/stores/user";
import { startChat} from "@/services/chatService";
import { UserOutlined , RobotOutlined} from '@ant-design/icons-vue';
import {message} from "ant-design-vue";

import { MdPreview } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
const id = 'preview-only';

const userStore = useUserStore();
const chatMessage = reactive({
  content: ''
})

const loading = ref<boolean>(false);
const chatRecord = ref<Array<any>>([]);

onMounted(() => {
  console.log(userStore.userName, userStore.userId)
})
async function chat(){
  loading.value = true;
  const request = {'role': 'person', 'content': chatMessage.content};
  chatRecord.value.push(request);
  const res = await startChat(userStore.userId, chatMessage);
  loading.value = false;
  if(res.code === 200){
    const response = {'role': 'robot', 'content': res.output.content}
    chatRecord.value.push(response);
    chatMessage.content = '';
  }
  else{
    message.error('edit fail: '+res.message);
  }

}
function edit(){
  router.push('/edit')
}
function logout(){
  router.push('/')
}
</script>
<style scoped lang="css">

.chat-container{
  width: 90%;
  margin-left: 5%;
  height: 700px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 2px;
  overflow: auto;
}

.robot-div{
  background-color: lightcyan;
  margin-top: 5px;
  max-width: 90%;
  margin-left: 10px;
  border-radius: 4px;
}
.person-div{
  background-color: cornflowerblue;
  margin-top: 5px;
  max-width: 90%;
  margin-left: 10px;
  border-radius: 4px;
}
</style>
