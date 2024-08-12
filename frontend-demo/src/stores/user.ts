import {defineStore} from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({
        userId: 0,
        userName: '',
        telephone: '',
    }),
    actions: {
        setUserInfo(user_id: any, user_name: string, telephone: string) {
            console.log('------- set user info')
            this.userId = user_id;
            this.userName = user_name;
            this.telephone = telephone;
        }
    },
    getters: {},
    persist:{
        key: 'userStore',
        storage: localStorage,
        paths:['userId', 'userName', 'telephone']
    }
})
