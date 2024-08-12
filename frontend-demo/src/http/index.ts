import axios from 'axios'
// 创建axios实例
const request = axios.create({
    baseURL: 'http://localhost:8000',// 所有的请求地址前缀部分
    timeout: 80000, // 请求超时时间(毫秒)
})

// request拦截器
request.interceptors.request.use(
    config => {
        return config
    },
    error => {
        Promise.reject(error)
    }
)

// response 拦截器
request.interceptors.response.use(
    response => {
        return response.data
    },
    error => {
        return Promise.reject(error)
    }
)
export default request
