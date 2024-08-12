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
          <a-button style="width: 100%" @click="register">注册</a-button>
        </a-col>
      </a-row>
    </div>
  </a-flex>
</template>

<script lang="ts" setup>

import {reactive} from "vue";
import {userRegister} from "@/services/userService";
import { message } from 'ant-design-vue';
const registerMessage = reactive({
  user_name:'',
  password: '',
  telephone:'',
})


async function register(){
  let res = await userRegister(registerMessage)
  if(res.code === 200){
    message.success('register success');
  }
  else{
    message.error('register fail: '+res.message);
  }
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
