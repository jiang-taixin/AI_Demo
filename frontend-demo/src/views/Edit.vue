<template>
  <a-flex vertical justify="center" align="center" style="height: 100%">
    <div class="login_container">
      <a-row :gutter="20">
        <a-col :span="2" :offset="4">
          用户名：
        </a-col>
        <a-col :span="14">
          <a-input v-model:value="registerMessage.user_name" />
        </a-col>
      </a-row>
      <a-row :gutter="20">
        <a-col :span="2" :offset="4">
          密码：
        </a-col>
        <a-col :span="14">
          <a-input v-model:value="registerMessage.password" />
        </a-col>
      </a-row>
      <a-row :gutter="20">
        <a-col :span="2" :offset="4">
          手机号：
        </a-col>
        <a-col :span="14">
          <a-input v-model:value="registerMessage.telephone" />
        </a-col>
      </a-row>

      <a-row :gutter="20" style="margin-top: 20px">
        <a-col :span="7" :offset="6">
          <a-button style="width: 100%" @click="edit">修改</a-button>
        </a-col>
        <a-col :span="7">
          <a-button style="width: 100%" @click="login">去登录</a-button>
        </a-col>
      </a-row>
    </div>
  </a-flex>
</template>

<script lang="ts" setup>

import {onMounted, reactive} from "vue";
import {userRegister, getUser, userEdit} from "@/services/userService";
import { message } from 'ant-design-vue';

import { useUserStore } from "@/stores/user";
import router from "@/router";
const userStore = useUserStore();

const registerMessage = reactive({
  user_name:'',
  password: '',
  telephone:'',
})

onMounted(async () => {
  const res =  await getUser(userStore.userId);
  if(res.code === 200){
    registerMessage.user_name = res.user.user_name;
    registerMessage.telephone = res.user.telephone;
    registerMessage.password = res.user.password;
  }
  else{
    message.error('edit fail: '+res.message);
  }
})

async function edit(){
  let res = await userEdit(registerMessage, userStore.userId);
  if(res.code === 200){
    message.success('edit success');
  }
  else{
    message.error('edit fail: '+res.message);
  }
}

async function login(){
  router.push('/')
}


</script>

<style scoped lang="scss">

.login_container{
  width: 60%;
  background-color: #2c3e50;
  border-radius: 4px;
  box-shadow: 0 0 2px;
  color: white;
  padding-top: 50px;
  padding-bottom: 50px;
}

.ant-row{
  align-items: center;
  margin-top: 5px;
}

</style>
